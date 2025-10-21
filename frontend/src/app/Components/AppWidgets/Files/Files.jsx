"use client";
import React, { useEffect, useState } from "react";
import { Avatar, List } from "antd";
import {
  EditOutlined,
  FileOutlined,
  FileTextOutlined,
  FileWordOutlined,
  FileZipOutlined,
} from "@ant-design/icons";
import Link from "next/link";
import axios from "axios";
import Widget from "@/app/Common/Widget";
import moment from "moment";

// NextCloud
function Files() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    const fetchDocs = async () => {
      try {
        const res = await axios.get("/api/v1/ocs/activities");
        setFiles(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, []);

  const onSearch = async (value) => {
    try {
      const res = await axios.get(`/api/v1/ocs/search?term=${value}`);
      setFiles(res.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <Widget
      title="Bestanden"
      setSearch={onSearch}
      loading={loading}
      error={error}
    >
      <List
        dataSource={files}
        renderItem={(item) => (
          <List.Item key={item.datetime}>
            <List.Item.Meta
              avatar={
                <Avatar
                  icon={<FileOutlined />}
                  style={{ backgroundColor: "#1677ff" }}
                />
              }
              title={<Link href={item?.url}>{item.object_filename}</Link>}
              description={
                <span>
                  Gemaakt op:
                  {moment(item.datetime)?.format("DD-mm-YYYY HH:mm")}
                </span>
              }
            />
            <Link href="/#">
              <EditOutlined />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Files;

const data = [
  {
    createdAt: "2025-04-26T19:13:38.338Z",
    name: "Transcript_klacht.doc",
    avatar: <Avatar icon={<FileWordOutlined />} />,
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
    avatar: <Avatar icon={<FileZipOutlined />} />,
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
