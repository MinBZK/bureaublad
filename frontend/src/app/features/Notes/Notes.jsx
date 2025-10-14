"use client";
import React, { useState, useEffect } from "react";
import { Avatar, List } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import { baseUrl } from "@/app/Common/pageConfig";
import axios from "axios";
import Widget from "../../Common/Widget";

// Docs
function Note() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [favorite, setFavorite] = useState(false);
  const [search, setSearch] = useState("");
  useEffect(() => {
    setLoading(true);
    const fetchDocs = async () => {
      try {
        const res = await axios.get(
          `${baseUrl}/api/v1/docs/documents?favorite=${favorite}&title=${search}`,
        );
        setDocs(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, [favorite, search]);

  return (
    <Widget
      title="Notities"
      favorite={favorite}
      setFavorite={setFavorite}
      search={search}
      setSearch={setSearch}
      loading={loading}
      error={error}
    >
      <List
        dataSource={docs}
        renderItem={(item) => (
          <List.Item key={item.description}>
            <List.Item.Meta
              avatar={<Avatar icon={<FileTextOutlined />} />}
              title={<Link href={item?.url}>{item.title}</Link>}
              description={`Geüpdatet: ${item.updated_date}`}
            />
            <Link href={item?.url}>
              <EditOutlined />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Note;
