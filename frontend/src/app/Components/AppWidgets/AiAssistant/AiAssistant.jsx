"use client";
import React, { useState, useEffect, useRef } from "react";
import { Card, Result, Input, Timeline } from "antd";
import axios from "axios";
import { ArrowDownOutlined, SendOutlined } from "@ant-design/icons";
import moment from "moment";
import Widget from "@/app/Common/Widget";

const { Search } = Input;
function AiAssistant() {
  const [aiResult, setAiResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showArrow, setShowArrow] = useState(false);
  const timelineRef = useRef(null);

  useEffect(() => {
    // Show arrow only if there are more than 6 items
    if (aiResult?.length > 6) {
      setShowArrow(true);
    }

    const handleScroll = () => {
      const el = timelineRef.current;
      if (!el) return;

      // Check if user scrolled to bottom (with a small tolerance)
      const atBottom = el.scrollTop + el.clientHeight >= el.scrollHeight - 5;
      setShowArrow(!atBottom);
    };

    const el = timelineRef.current;
    if (el) el.addEventListener("scroll", handleScroll);

    return () => {
      if (el) el.removeEventListener("scroll", handleScroll);
    };
  }, [aiResult]);

  const postAi = (text) => {
    setLoading(true);
    const fetchDocs = async () => {
      try {
        const res = await axios.post("/api/v1/ai/chat/completions", {
          prompt: text,
        });
        setAiResult((arr) => [...arr, res.data]);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  };
  const items = aiResult?.map((value) => ({
    children: value,
    label: moment().format("DD-MM-YYYY HH:mm"),
  }));

  return (
    <Widget
      title="AI Assistant"
      loading={false}
      error={error}
      setSearch={(t) => postAi(t)}
    >
      <React.Fragment>
        {aiResult?.length > 0 && (
          <>
            <div
              ref={timelineRef}
              style={{
                marginTop: 30,
                maxHeight: 250,
                overflowY: "auto",
                paddingRight: 8,
              }}
            >
              <Timeline items={items} mode="left" reverse={true} />
            </div>
            <div
              style={{
                textAlign: "center",
                marginLeft: "-6px",
                visibility: showArrow ? "visible" : "hidden",
              }}
            >
              <ArrowDownOutlined
                style={{
                  fontSize: 24,
                  color: "#888",
                  animation: "bounce 1.2s infinite",
                }}
              />
            </div>
          </>
        )}
      </React.Fragment>
    </Widget>
  );
}

export default AiAssistant;
