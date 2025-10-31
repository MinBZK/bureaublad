"use client";
import React, { useState } from "react";
import { Avatar, List } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "../../../Common/Widget";
import { useFetchWithRefresh } from "../../../Common/CustomHooks/useFetchWithRefresh";

// Docs
function Note() {
  const [favorite, setFavorite] = useState(false);
  const [search, setSearch] = useState("");

  const {
    data: docs,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/docs/documents", {
    favorite,
    title: search,
  });

  return (
    <Widget
      title="Notities"
      favorite={favorite}
      setFavorite={setFavorite}
      search={search}
      setSearch={setSearch}
      error={error}
      onRefresh={onRefresh}
    >
      <List
        dataSource={docs}
        loading={loading}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.description}>
              <List.Item.Meta
                avatar={<Avatar icon={<FileTextOutlined />} />}
                title={<Link href={item?.url}>{item.title}</Link>}
                description={`Laatste wijziging: ${item.updated_date}`}
              />
              <Link href={item?.url}>
                <EditOutlined />
              </Link>
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default Note;
