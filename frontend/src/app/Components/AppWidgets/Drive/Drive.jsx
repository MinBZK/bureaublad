"use client";
import React, { useState } from "react";
import { Avatar, List } from "antd";
import { FileImageOutlined } from "@ant-design/icons";
import Link from "next/link";
import moment from "moment";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import { useTranslations } from "../../../../i18n/TranslationsProvider";

function Drive({ title = "Drive" }) {
  const [favorite, setFavorite] = useState(false);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const t = useTranslations("Drive");
  const {
    data: drive,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/drive/documents", {
    title: search,
    favorite,
    page,
    page_size: 3,
  });

  return (
    <Widget
      title={title}
      favorite={favorite}
      setFavorite={setFavorite}
      setSearch={setSearch}
      error={error}
      onRefresh={onRefresh}
      page={page}
      setPage={setPage}
      total={drive?.count}
    >
      <List
        className="widget-list"
        dataSource={drive?.results || []}
        loading={loading}
        renderItem={(item) => (
          <List.Item key={item.description}>
            <List.Item.Meta
              avatar={
                <Avatar icon={<FileImageOutlined />} className="avt-name" />
              }
              title={
                <Link
                  href={item?.url || ""}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item.title}
                </Link>
              }
              description={`${t("lastModified")}:${moment(item.updated_at).format("DD-MM-YYYY, mm:ss")}`}
            />
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Drive;
