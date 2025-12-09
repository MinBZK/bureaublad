"use client";
import React, { useState } from "react";
import { Avatar, List } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "../../../Common/Widget";
import { useFetchWithRefresh } from "../../../Common/CustomHooks/useFetchWithRefresh";

// Docs
function Documents({ title = "Docs" }) {
  const [favorite, setFavorite] = useState(false);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const {
    data: docs,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/docs/documents", {
    favorite,
    title: search,
    page,
    page_size: 3,
  });
  return (
    <Widget
      title={title}
      favorite={favorite}
      setFavorite={setFavorite}
      search={search}
      setSearch={setSearch}
      error={error}
      onRefresh={onRefresh}
      page={page}
      setPage={setPage}
      total={docs?.count}
    >
      <List
        className="widget-list"
        dataSource={docs?.results || []}
        loading={loading}
        renderItem={(item) => (
          <List.Item key={item.description}>
            <List.Item.Meta
              avatar={<Avatar icon={<FileTextOutlined />} />}
              title={
                <Link
                  href={item?.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item.title}
                </Link>
              }
              description={`Laatste wijziging: ${item.updated_date}`}
            />
            <Link href={item?.url} target="_blank" rel="noopener noreferrer">
              <EditOutlined />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Documents;
