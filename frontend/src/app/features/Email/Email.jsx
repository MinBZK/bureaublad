"use client";
import React from "react";
import { Card } from "antd";
import { Avatar, List } from "antd";
import { EditOutlined, MailOutlined } from "@ant-design/icons";
import Link from "next/link";

function Email() {
  return (
    <Card title="Email" variant="borderless">
      <List
        dataSource={data}
        renderItem={(item) => (
          <List.Item key={item.email}>
            <List.Item.Meta
              avatar={<Avatar src={item.avatar} />}
              title={<a href="https://ant.design">{item.name}</a>}
              description={item.email}
            />
            <Link href="/#">
              <EditOutlined />
            </Link>
          </List.Item>
        )}
      />
    </Card>
  );
}

export default Email;

const data = [
  {
    createdAt: "2025-04-26T19:13:38.338Z",
    name: "Transcript klacht ",
    avatar: <Avatar icon={<MailOutlined />} />,
    gender: "female",
    email: "youngboizzz@gmail.com",
    city: "Lake Lorenzo",
    birthdate: "1955-04-13T21:25:22.777Z",
    id: "7",
    address: "Lake Lorenzo",
  },
  {
    createdAt: "2025-04-27T03:03:49.295Z",
    name: "Lizeth Hagenes klacht",
    avatar: <Avatar icon={<MailOutlined />} />,
    gender: "male",
    email: "Lizeth_Hagenes@hotmail.com",
    city: "Franeckitown",
    birthdate: "1964-07-01T13:57:11.140Z",
    id: "8",
  },
  {
    createdAt: "2025-04-27T12:14:11.838Z",
    name: "Terence Hilpert",
    avatar: <Avatar icon={<MailOutlined />} />,
    gender: "female",
    email: "Alva_Tillman@gmail.com",
    city: "North Aimee",
    birthdate: "1979-01-14T21:17:21.365Z",
    id: "9",
  },
];
