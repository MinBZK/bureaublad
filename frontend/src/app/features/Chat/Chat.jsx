"use client";
import React from "react";
import { Card } from "antd";

import { Avatar, List } from "antd";
import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";

function Chat() {
  return (
    <Card title="Chat" variant="borderless">
      <List
        dataSource={data}
        renderItem={(item) => (
          <List.Item key={item.email}>
            <List.Item.Meta
              avatar={<Avatar src={item.avatar} />}
              title={<a href="/#">{item.name}</a>}
              description={item.email}
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
    </Card>
  );
}

export default Chat;

const data = [
  {
    createdAt: "2025-04-26T19:13:38.338Z",
    name: "Let go boizz",
    avatar: "https://api.dicebear.com/7.x/miniavs/svg?seed=1",
    gender: "female",
    email: "youngboizzz@gmail.com",
    city: "Lake Lorenzo",
    birthdate: "1955-04-13T21:25:22.777Z",
    id: "7",
    address: "Lake Lorenzo",
  },
  {
    createdAt: "2025-04-27T03:03:49.295Z",
    name: "Lizeth Friesen",
    avatar: "https://api.dicebear.com/7.x/miniavs/svg?seed=2",
    gender: "male",
    email: "Lizeth_Hagenes@hotmail.com",
    city: "Franeckitown",
    birthdate: "1964-07-01T13:57:11.140Z",
    id: "8",
  },
  {
    createdAt: "2025-04-27T12:14:11.838Z",
    name: "Terence Hilpert II",
    avatar: "https://api.dicebear.com/7.x/miniavs/svg?seed=3",
    gender: "female",
    email: "Alva_Tillman@gmail.com",
    city: "North Aimee",
    birthdate: "1979-01-14T21:17:21.365Z",
    id: "9",
  },
];
