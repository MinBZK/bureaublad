"use client";
import { useState } from "react";
import Widget from "@/app/Common/Widget";

function AiAssistant() {
  const [aiResult, setAiResult] = useState([]);
  const [error, setError] = useState("");

  const postAi = async (text) => {
    setError(null);
    setAiResult([]);

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

        // Each SSE message ends with \n\n
        let boundary = buffer.indexOf("\n\n");
        while (boundary !== -1) {
          const raw = buffer.slice(0, boundary).trim();
          buffer = buffer.slice(boundary + 2);
          boundary = buffer.indexOf("\n\n");

          if (!raw) continue;

          try {
            const data = JSON.parse(raw);
            if (data.finish_reason === "stop") break;

            // Append streamed content
            if (data.content) {
              finalText += data.content;
              setAiResult((prev) => [...prev.slice(0, -1), finalText]);
            } else if (prev.length === 0) {
              // Initialize first chunk
              setAiResult([data.content || ""]);
            }
          } catch (err) {
            console.error("Skipping invalid chunk:", raw, err);
          }
        }
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  return (
    <Widget
      title="AI Assistant"
      loading={false}
      error={error}
      setSearch={(t) => postAi(t)}
    >
      {aiResult.map((msg, i) => (
        <div key={i} className="message">
          {msg}
        </div>
      ))}
    </Widget>
  );
}

export default AiAssistant;
