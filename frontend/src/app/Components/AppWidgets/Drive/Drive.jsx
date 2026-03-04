"use client";
import React, { useState } from "react";
import { FileImageOutlined } from "@ant-design/icons";
import Link from "next/link";
import moment from "moment";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import { useTranslations } from "../../../../i18n/TranslationsProvider";
import CustomList from "@/app/Common/CustomList";

function Drive({ app }) {
  // const [favorite, setFavorite] = useState(false);
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
    // favorite,
    page,
    page_size: 3,
  });

  return (
    <Widget
      title={t("title")}
      app={app}
      // favorite={favorite}
      // setFavorite={setFavorite}
      setSearch={setSearch}
      error={error}
      onRefresh={onRefresh}
      page={page}
      setPage={setPage}
      total={drive?.count}
    >
      <CustomList
        className="widget-list"
        dataSource={drive?.results || []}
        loading={loading}
        renderItem={(item, index) =>
          index < 3 && (
            <CustomList.Item key={item.id}>
              <CustomList.Item.Meta
                avatar={<FileImageOutlined className="widget-icon-orange" />}
                title={
                  <Link
                    href={item?.url || ""}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {item.title}
                  </Link>
                }
                description={`${t("lastModified")}: ${moment.utc(item.updated_at).format("DD-MM-YYYY, HH:mm")}`}
              />
            </CustomList.Item>
          )
        }
      />
    </Widget>
  );
}

export default Drive;
