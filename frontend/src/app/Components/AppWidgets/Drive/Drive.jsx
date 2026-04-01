"use client";
import { useState } from "react";
import { useLocalStorage } from "@/app/Common/CustomHooks/useLocalStorage";
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
  const [isFavorite, setIsFavorite] = useLocalStorage(
    "drive_is_favorite",
    false,
  );
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
    is_favorite: isFavorite || undefined,
    page,
    page_size: 3,
  });

  return (
    <Widget
      app={app}
      favorite={isFavorite}
      setFavorite={setIsFavorite}
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
        search={search}
        renderItem={(item, index) =>
          index < 3 && (
            <CustomList.Item key={item?.id}>
              <CustomList.Item.Meta
                avatar={
                  <Avatar
                    icon={fileIcon(item?.mimetype)}
                    className="avt-name"
                    style={{
                      backgroundColor: fileBackgroundColor(item?.mimetype),
                    }}
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

const MIME_ICON_CONFIG = [
  ["image", FileImageOutlined, "#7719AA"],
  ["text", FileTextOutlined, "#185ABD"],
  ["spreadsheet", FileExcelOutlined, "#107C41"],
  ["presentation", FilePptOutlined, "#C43E1C"],
];

const fileIcon = (mimetype) => {
  const [, Icon = FileOutlined] =
    MIME_ICON_CONFIG.find(([type]) => mimetype?.includes(type)) ?? [];
  return <Icon style={{ color: "#ffffff" }} />;
};

const fileBackgroundColor = (mimetype) => {
  const [, , backgroundColor = "#8c8c8c"] =
    MIME_ICON_CONFIG.find(([type]) => mimetype?.includes(type)) ?? [];
  return backgroundColor;
};
