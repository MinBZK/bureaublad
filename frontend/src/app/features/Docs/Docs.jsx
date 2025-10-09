"use client";
import React, { useState, useEffect } from "react";
import { Card } from "antd";
import { Avatar, List } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import { baseUrl } from "@/app/Common/pageConfig";

function Docs() {
  const [docs, setDocs] = useState([]);
  useEffect(() => {
    fetch(baseUrl + "/api/v1/docs/documents", {
      method: "GET",
      mode: "cors",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        // Authorization: `Bearer ${keycloak.token}`,
      },
    })
      .then((res) => res.json())
      .then((json) => setDocs(json))
      .catch((err) => console.error("Fetch error:", err));
  }, []);
  console.log(docs);
  return (
    <Card title="Docs" variant="borderless">
      <List
        dataSource={data}
        renderItem={(item) => (
          <List.Item key={item.description}>
            <List.Item.Meta
              avatar={<Avatar src={item.avatar} />}
              title={<a href="https://ant.design">{item.name}</a>}
              description={item.description}
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

export default Docs;

const data = [
  {
    createdAt: "2025-04-26T19:13:38.338Z",
    name: "Transcript_klacht.doc",
    avatar: <Avatar icon={<FileTextOutlined />} />,
    gender: "female",
    description: "Word",
    city: "Lake Lorenzo",
    birthdate: "1955-04-13T21:25:22.777Z",
    id: "7",
    address: "Lake Lorenzo",
  },
  {
    createdAt: "2025-04-27T03:03:49.295Z",
    name: "Lizeth_Hagenes_klacht.doc",
    avatar: <Avatar icon={<FileTextOutlined />} />,
    gender: "male",
    description: "Word",
    city: "Franeckitown",
    birthdate: "1964-07-01T13:57:11.140Z",
    id: "8",
  },
  {
    createdAt: "2025-04-27T12:14:11.838Z",
    name: "Terence_Hilpert.doc",
    avatar: <Avatar icon={<FileTextOutlined />} />,
    gender: "female",
    description: "Word",
    city: "North Aimee",
    birthdate: "1979-01-14T21:17:21.365Z",
    id: "9",
  },
];
