"use client";
import React, { useState, useEffect } from "react";

import { Avatar, List } from "antd";
import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import axios from "axios";
import moment from "moment";

// Conversation
function Conversations() {
  const [conv, setConv] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    const fetchChat = async () => {
      try {
        const res = await axios.get(`/api/v1/conversations/chats?page=1`);
        setConv(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchChat();
  }, []);
  return (
    <Widget title="Gesprekken" loading={loading} error={error}>
      <List
        dataSource={conv}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.id}>
              <List.Item.Meta
                title={<Link href={item?.url}>{item.title}</Link>}
                description={
                  <span>
                    Gemaakt op:
                    {moment(item.created_at)?.format("DD-mm-YYYY HH:mm")}
                  </span>
                }
              />
              <Link href={item?.url}>
                <Avatar
                  style={{ backgroundColor: "#1677ff" }}
                  icon={<WechatOutlined />}
                />
              </Link>
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default Conversations;
