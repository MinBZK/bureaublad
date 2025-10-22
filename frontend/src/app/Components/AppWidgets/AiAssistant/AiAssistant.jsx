"use client";
import React, { useState } from "react";
import { Card, Result, Input, Timeline } from "antd";
import axios from "axios";
import { ArrowDownOutlined, SendOutlined } from "@ant-design/icons";
import moment from "moment";

const { Search } = Input;
function AiAssistant() {
  const [aiResult, setAiResult] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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
    <Card title="AiAssistant" variant="borderless">
      <React.Fragment>
        <Search
          placeholder="Ask anything"
          enterButton={<SendOutlined />}
          onSearch={postAi}
        />
        {aiResult?.length > 0 && (
          <React.Fragment>
            <div className="position-timeline ">
              <Timeline items={items} mode="left" reverse={true} />
            </div>
            {aiResult?.length > 6 && (
              <div className="position-scrol-down">
                <ArrowDownOutlined className="scrol-down-icon" />
              </div>
            )}
          </React.Fragment>
        )}
        {error && (
          <Result status="warning" title={error} className="space-min-up" />
        )}
      </React.Fragment>
    </Card>
  );
}

export default AiAssistant;
