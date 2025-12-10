"use client";
import React, { useState } from "react";
import { Button, Divider, Drawer, Input, Result } from "antd";
import { RobotOutlined } from "@ant-design/icons";
import ReactMarkdown from "react-markdown";
const { Search } = Input;
function AiAssistant() {
  const [open, setOpen] = useState(false);
  const [aiResult, setAiResult] = useState([]);
  const [error, setError] = useState("");

  const postAi = async (text) => {
    setError(null);
    setAiResult([]);
    if (text === "") return;

    try {
      const response = await fetch("/api/v1/ai/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "text/event-stream",
        },
        body: JSON.stringify({ prompt: text }),
      });

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
        title="Ai Assistent"
        closable={{ "aria-label": "Close Button" }}
        onClose={() => setOpen(false)}
        open={open}
      >
        {error ? (
          <Result status="warning" title={error} className="space-min-up" />
        ) : (
          <React.Fragment>
            <Search
              placeholder={"Typ je vraag hier..."}
              onSearch={(t) => postAi(t)}
              allowClear
              className="widget-search"
            />
            <Divider />
            {aiResult.map((msg, i) => (
              <div key={i} className="message">
                <ReactMarkdown>{msg}</ReactMarkdown>
              </div>
            ))}
          </React.Fragment>
        )}
      </Drawer>
    </>
  );
}

export default AiAssistant;
