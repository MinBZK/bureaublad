"use client";
import React, { useState, useEffect } from "react";
import { Avatar, List } from "antd";
import { PhoneOutlined } from "@ant-design/icons";
import Widget from "@/app/Common/Widget";
import axios from "axios";
import Link from "next/link";

// meet
function VideoChat() {
  const [meet, setMeet] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");
  useEffect(() => {
    setLoading(true);
    const fetchMeet = async () => {
      try {
        const res = await axios.get(`/api/v1/meet/rooms?page=1`);
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
    <Widget
      title="Video Chat"
      loading={loading}
      error={error}
      search={search}
      setSearch={setSearch}
    >
      <List
        dataSource={meet.filter((item) =>
          item.name.toLowerCase().includes(search.toLowerCase()),
        )}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.slug}>
              <List.Item.Meta
                avatar={
                  <Avatar className="avt-name">
                    {item?.name?.at(0)?.toUpperCase()}
                  </Avatar>
                }
                title={<Link href={item.url}>{item.name}</Link>}
                description={<span>Hostsleutel:{item.pin_code}</span>}
              />
              <Link href={item.url}>
                <Avatar className="avt-call" icon={<PhoneOutlined />} />
              </Link>
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default VideoChat;
