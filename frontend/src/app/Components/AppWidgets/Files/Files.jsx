"use client";
import React, { useState } from "react";
import { EditOutlined, FileOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import moment from "moment";
import { useTranslations } from "@/i18n/TranslationsProvider";
import CustomList from "@/app/Common/CustomList";

// NextCloud
function Files({ app }) {
  const [searchTerm, setSearchTerm] = useState("");
  const t = useTranslations("Files");
  const [page, setPage] = useState(1);

  const {
    data: files,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh(searchTerm ? "/ocs/search" : "/ocs/activities", {
    term: searchTerm,
  });

  const onSearch = (value) => {
    setSearchTerm(value);
  };
  const filteredFiles =
    files?.results?.flatMap((value) =>
      value?.files?.map((file) => ({ ...file, datetime: value?.datetime })),
    ) ?? [];

  const uniqueFiles =
    Array.from(
      new Map(filteredFiles?.map((item) => [item?.id, item])).values(),
    ) ?? [];

  const paginatedFiles = uniqueFiles?.slice((page - 1) * 3, page * 3) ?? [];
  return (
    <Widget
      title={t("title")}
      app={app}
      setSearch={onSearch}
      error={error}
      onRefresh={onRefresh}
      page={page}
      setPage={setPage}
      total={uniqueFiles?.length}
    >
      <CustomList
        dataSource={paginatedFiles}
        loading={loading}
        className="widget-list"
        renderItem={(item) => (
          <CustomList.Item key={item?.id}>
            <CustomList.Item.Meta
              avatar={<FileOutlined className="widget-icon-blue" />}
              title={
                <Link
                  href={item?.link}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item?.name}
                </Link>
              }
              description={
                <span>
                  {t("lastModified")}:
                  {moment(item?.datetime).format("DD-MM-YYYY, HH:mm")}
                </span>
              }
            />
            <Link href={item?.link} target="_blank" rel="noopener noreferrer">
              <EditOutlined />
            </Link>
          </CustomList.Item>
        )}
      />
    </Widget>
  );
}

export default Files;
