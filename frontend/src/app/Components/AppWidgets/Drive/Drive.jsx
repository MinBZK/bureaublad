"use client";
import React, { useState } from "react";
import { Avatar } from "antd";
import {
  FileExcelOutlined,
  FileImageOutlined,
  FileOutlined,
  FilePptOutlined,
  FileTextOutlined,
} from "@ant-design/icons";
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
            <CustomList.Item key={item?.id}>
              <CustomList.Item.Meta
                avatar={
                  <Avatar
                    icon={fileIcon(item?.mimetype)}
                    className="avt-name"
                  />
                }
                title={
                  <Link
                    href={item?.url_preview || ""}
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

const MIME_ICONS = [
  ["image", FileImageOutlined],
  ["text", FileTextOutlined],
  ["spreadsheet", FileExcelOutlined],
  ["presentation", FilePptOutlined],
];

const fileIcon = (mimetype) => {
  const Icon =
    MIME_ICONS.find(([type]) => mimetype?.includes(type))?.[1] ?? FileOutlined;
  return <Icon />;
};
