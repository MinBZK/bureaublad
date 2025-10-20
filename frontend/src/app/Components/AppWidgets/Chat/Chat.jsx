"use client";
import React, { useState, useEffect } from "react";

import { Avatar, List } from "antd";
import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import moment from "moment";
import axios from "axios";

function Chat() {
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    const fetchChat = async () => {
      try {
        const res = await axios.get(`/api/v1/conversations/chats`);
        console.log(res);
        setChat(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchChat();
  }, []);

  return (
    <Widget title="Chat" loading={loading} error={error}>
      <List
        dataSource={chat}
        renderItem={(item) => (
          <List.Item key={item.id}>
            <List.Item.Meta
              title={<Link href="/#">{item.content}</Link>}
              description={
                <span>
                  Gemaakt op:
                  {moment(item?.created_at).format("DD-MM-yyyy HH:mm")}
                </span>
              }
            />
            <Link href="/#">
              <Avatar
                style={{ backgroundColor: "#1677ff" }}
                icon={<WechatOutlined />}
              />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Chat;
