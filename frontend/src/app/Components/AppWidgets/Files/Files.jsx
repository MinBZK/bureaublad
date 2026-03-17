"use client";
import React, { useState } from "react";
import { Avatar } from "antd";
import {
  EditOutlined,
  FileExcelOutlined,
  FileImageOutlined,
  FileOutlined,
  FilePptOutlined,
  FileWordOutlined,
} from "@ant-design/icons";
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
        renderItem={(item) => {
          const { Icon, backgroundColor } = fileVisualByExtension(item?.name);

          return (
            <CustomList.Item key={item?.id}>
              <CustomList.Item.Meta
                avatar={
                  <Avatar
                    icon={<Icon style={{ color: "#ffffff" }} />}
                    className="avt-doc"
                    style={{ backgroundColor }}
                  />
                }
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
                  item?.datetime && (
                    <span>
                      {t("lastModified")}:{" "}
                      {moment(item?.datetime).format("DD-MM-YYYY, HH:mm")}
                    </span>
                  )
                }
              />
              <Link href={item?.link} target="_blank" rel="noopener noreferrer">
                <EditOutlined />
              </Link>
            </CustomList.Item>
          );
        }}
      />
    </Widget>
  );
}

export default Files;

const EXTENSION_VISUALS = [
  {
    extensions: ["png", "jpg", "jpeg"],
    Icon: FileImageOutlined,
    backgroundColor: "#7719AA",
  },
  {
    extensions: ["doc", "docx", "odt", "odf"],
    Icon: FileWordOutlined,
    backgroundColor: "#185ABD",
  },
  {
    extensions: ["xls", "xlsx", "ods"],
    Icon: FileExcelOutlined,
    backgroundColor: "#107C41",
  },
  {
    extensions: ["ppt", "pptx", "odp"],
    Icon: FilePptOutlined,
    backgroundColor: "#C43E1C",
  },
];

const fileVisualByExtension = (filename) => {
  const extension = filename?.split(".")?.pop()?.toLowerCase();

  const visual = EXTENSION_VISUALS.find(({ extensions }) =>
    extensions.includes(extension),
  );

  return visual ?? { Icon: FileOutlined, backgroundColor: "#8c8c8c" };
};
