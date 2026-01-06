"use client";
import React, { useState } from "react";
import { Avatar } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "../../../Common/Widget";
import { useFetchWithRefresh } from "../../../Common/CustomHooks/useFetchWithRefresh";
import { useTranslations } from "../../../../i18n/TranslationsProvider";
import CustomList from "../../../Common/CustomList";

// Docs
function Documents({ title = "Docs" }) {
  const [favorite, setFavorite] = useState(false);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const t = useTranslations("Documents");
  const {
    data: docs,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/docs/documents", {
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
      <CustomList
        className="widget-list"
        dataSource={docs?.results || []}
        loading={loading}
        renderItem={(item) => (
          <CustomList.Item key={item.id}>
            <CustomList.Item.Meta
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
              description={`${t("lastModified")}: ${item.updated_date}`}
            />
            <Link href={item?.url} target="_blank" rel="noopener noreferrer">
              <EditOutlined />
            </Link>
          </CustomList.Item>
        )}
      />
    </Widget>
  );
}

export default Documents;
