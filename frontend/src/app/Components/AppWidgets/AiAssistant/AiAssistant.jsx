"use client";
import React, { useState, useRef, useEffect } from "react";
import { Button, Divider, Drawer, Input, Result } from "antd";
import { RobotOutlined, SendOutlined } from "@ant-design/icons";
import ReactMarkdown from "react-markdown";
import { useTranslations } from "../../../../i18n/TranslationsProvider";
import {
  INITIAL_LOCALE,
  LOCALE_STORAGE_LANG_KEY,
} from "../../../../i18n/config";
const { TextArea } = Input;

function AiAssistant() {
  const t = useTranslations("AiAssistant");
  const [open, setOpen] = useState(false);
  const [aiResult, setAiResult] = useState([]);
  const [error, setError] = useState("");
  const [inputValue, setInputValue] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [aiResult]);

  const handleSubmit = () => {
    const text = inputValue.trim();
    if (!text) return;
    setInputValue("");
    postAi(text);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const postAi = async (text) => {
    setError(null);
    setAiResult([]);
    if (text === "") return;

    try {
      const response = await fetch("/api/v1/ai/chat/completions", {
        method: "POST",
        headers: {
          "Accept-Language":
            typeof window !== "undefined"
              ? localStorage.getItem(LOCALE_STORAGE_LANG_KEY) || INITIAL_LOCALE
              : INITIAL_LOCALE,
          "Content-Type": "application/json",
          Accept: "text/event-stream",
        },
        body: JSON.stringify({ prompt: text }),
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
          const errorData = await response.json();
          errorMessage = errorData.message || errorData.error || errorMessage;
        } catch {
          errorMessage = response.statusText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      if (!response.body) {
        throw new Error("No response body (SSE not supported?)");
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";
      let finalText = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        let boundary = buffer.indexOf("\n\n");
        while (boundary !== -1) {
          const raw = buffer.slice(0, boundary).trim();
          buffer = buffer.slice(boundary + 2);
          boundary = buffer.indexOf("\n\n");

          if (!raw) continue;

          try {
            const data = JSON.parse(raw);
            if (data.finish_reason === "stop") break;
            if (data.content) {
              finalText += data.content;
              setAiResult((prev) => [...prev.slice(0, -1), finalText]);
            } else if (data.length === 0) {
              setAiResult([data.content || ""]);
            }
          } catch (err) {
            console.error("Skipping invalid chunk:", raw, err);
          }
        }
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <>
      <Button
        color="default"
        variant="link"
        className="profile-link"
        onClick={() => setOpen(true)}
        size="large"
      >
        <RobotOutlined />
      </Button>
      <Drawer
        title={t("title")}
        closable={{ "aria-label": "Close Button" }}
        onClose={() => setOpen(false)}
        open={open}
        classNames={{
          body: `ai-drawer-body${aiResult.length === 0 && !error ? " ai-drawer-body--empty" : ""}`,
        }}
      >
        {(aiResult.length > 0 || !!error) && (
          <>
            <div className="ai-drawer-messages">
              {error ? (
                <Result
                  status="warning"
                  title={error}
                  className="space-min-up"
                />
              ) : (
                <React.Fragment>
                  {aiResult.map((msg, i) => (
                    <div key={i} className="message">
                      <ReactMarkdown>{msg}</ReactMarkdown>
                    </div>
                  ))}
                  <div ref={bottomRef} />
                </React.Fragment>
              )}
            </div>
            <Divider className="ai-drawer-divider" />
          </>
        )}
        <div className="ai-drawer-input">
          <TextArea
            placeholder={t("placeholder")}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            autoSize={{ minRows: 2, maxRows: 6 }}
            allowClear
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSubmit}
            className="ai-drawer-send"
          />
        </div>
      </Drawer>
    </>
  );
}

export default AiAssistant;
