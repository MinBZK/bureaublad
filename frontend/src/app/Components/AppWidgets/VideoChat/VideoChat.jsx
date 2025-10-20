"use client";
import React, { useState, useEffect } from "react";
import { Avatar, List } from "antd";
import { PhoneOutlined } from "@ant-design/icons";
import Widget from "@/app/Common/Widget";
import axios from "axios";

// meet
function VideoChat() {
  const [meet, setMeet] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    const fetchMeet = async () => {
      try {
        const res = await axios.get(`/api/v1/meet/rooms`);
        setMeet(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchMeet();
  }, []);
  return (
    <Widget title="Video Chat" loading={loading} error={error}>
      <List
        dataSource={meet}
        renderItem={(item) => (
          <List.Item key={item.slug}>
            <List.Item.Meta
              avatar={
                <Avatar
                  style={{
                    backgroundColor: "#f56a00",
                    verticalAlign: "middle",
                  }}
                >
                  {item?.name?.at(0)?.toUpperCase()}
                </Avatar>
              }
              title={<a href="/#">{item.name}</a>}
              description={<span>Hostsleutel:{item.pin_code}</span>}
            />
            <Avatar
              style={{ backgroundColor: "#87d068" }}
              icon={<PhoneOutlined />}
            />
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default VideoChat;
