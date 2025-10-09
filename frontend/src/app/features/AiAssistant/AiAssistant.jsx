"use client";
import React, { useState, useEffect } from "react";
import { Card, Result, Input, Timeline } from "antd";
import { baseUrl } from "@/app/Common/pageConfig";
import axios from "axios";
import { SendOutlined } from "@ant-design/icons";

const { Search } = Input;
function AiAssistant() {
  const [aiResult, setAiResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const postAi = (text) => {
    setLoading(true);
    const fetchDocs = async () => {
      try {
        const res = await axios.post(baseUrl + "/api/v1/ai/chat/completions", {
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
  }));

  return (
    <Card title="AiAssistant" variant="borderless">
      <React.Fragment>
        <Search
          placeholder="Ask anything"
          enterButton={<SendOutlined />}
          onSearch={postAi}
        />
        {aiResult?.length > 0 && (
          <Timeline style={{ marginTop: "30px" }} items={items} />
        )}
        {error && (
          <Result
            status="warning"
            title={error}
            style={{ marginTop: "-10%" }}
          />
        )}
      </React.Fragment>
    </Card>
  );
}

export default AiAssistant;
