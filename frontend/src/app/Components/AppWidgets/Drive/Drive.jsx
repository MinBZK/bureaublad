"use client";
import React, { useState } from "react";
import { Avatar, List } from "antd";
import { FileImageOutlined } from "@ant-design/icons";
import Link from "next/link";
import moment from "moment";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";

function Drive() {
  const [favorite, setFavorite] = useState(false);
  const [search, setSearch] = useState("");

  const {
    data: drive,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/drive/documents", {
    title: search,
    favorite,
  });

  return (
    <Widget
      title="Drive"
      favorite={favorite}
      setFavorite={setFavorite}
      setSearch={setSearch}
      error={error}
      onRefresh={onRefresh}
    >
      <List
        dataSource={drive}
        loading={loading}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.description}>
              <List.Item.Meta
                avatar={
                  <Avatar icon={<FileImageOutlined />} className="avt-name" />
                }
                title={<Link href={item?.url || ""}>{item.title}</Link>}
                description={`Laatste wijziging: ${moment(item.updated_at).format("DD-MM-YYYY, mm:ss")}`}
              />
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default Drive;
