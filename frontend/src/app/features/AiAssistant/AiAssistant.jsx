"use client";
import React, { useState, useEffect } from "react";
import { Card, Result, Input, Timeline } from "antd";
import { baseUrl } from "@/app/Common/pageConfig";
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
            <div
              style={{
                marginTop: 30,
                maxHeight: 250,
                overflowY: "auto",
                paddingRight: 8,
              }}
            >
              <Timeline items={items} mode="left" reverse={true} />
            </div>
            {aiResult?.length > 6 && (
              <div style={{ textAlign: "center", marginTop: 20 }}>
                <ArrowDownOutlined
                  style={{
                    fontSize: 24,
                    color: "#888",
                    animation: "bounce 1.2s infinite",
                  }}
                />
              </div>
            )}
          </React.Fragment>
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
