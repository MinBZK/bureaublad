"use client";
import React, { useState, useEffect } from "react";
import { Avatar, List } from "antd";
import { PhoneOutlined } from "@ant-design/icons";
import Widget from "@/app/Common/Widget";
import axios from "axios";
import { baseUrl } from "@/app/Common/pageConfig";

// meet
function VideoChat() {
  const [meet, setMeet] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => {
    setLoading(true);
    const fetchMeet = async () => {
      try {
        const res = await axios.get(`${baseUrl}/api/v1/meet/rooms`);
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
    <Widget title="Video Chat" loading={loading} error={null}>
      <List
        dataSource={data}
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
              title={<a href="https://ant.design">{item.name}</a>}
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

const data = [
  {
    id: "3fa85f64-5717-b3fc-4562-b3fc-2c963f66afa6",
    name: "abz-rlzz-itv",
    slug: "abz-rlzz-itv",
    configuration: "{}",
    access_level: "public",
    pin_code: "3fa85f64",
  },
  {
    id: "3fa85f64-5717-4562-b3fc-b3fc-2c963f66afa6",
    name: "itv-abz-rlzz",
    slug: "itv-abz-rlzz",
    configuration: "{}",
    access_level: "public",
    pin_code: "5717-4562",
  },
  {
    id: "3fa85f64-5717-4562-b3fc-b3fc-2c963f66afa6",
    name: "rlzz-abz-itv",
    slug: "rlzz-abz-itv",
    configuration: "{}",
    access_level: "public",
    pin_code: "b3fc-b3fc",
  },
];
