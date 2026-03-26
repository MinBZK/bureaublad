"use client";
import { useState } from "react";
import { Avatar, Tooltip } from "antd";
import {
  GlobalOutlined,
  LockOutlined,
  PhoneOutlined,
  TeamOutlined,
} from "@ant-design/icons";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import Link from "next/link";
import { useTranslations } from "@/i18n/TranslationsProvider";
import CustomList from "@/app/Common/CustomList";

const ACCESS_LEVEL_ICON = {
  public: <GlobalOutlined />,
  trusted: <TeamOutlined />,
  restricted: <LockOutlined />,
};

// meet
function Meet({ app }) {
  // TODO search functionality is implemented in the frontend only because Meet dose not support search
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const t = useTranslations("Meet");
  const { data: meet, error, onRefresh } = useFetchWithRefresh("/meet/rooms");

  // Custom Pagination because meet dose not support pagination correctly
  const paginatedMeet = meet?.results?.slice((page - 1) * 3, page * 3) ?? [];

  return (
    <Widget
      app={app}
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
      page={page}
      setPage={setPage}
      total={meet?.count || 0}
    >
      <CustomList
        className="widget-list"
        dataSource={
          paginatedMeet?.filter((value) =>
            value?.name?.toUpperCase()?.includes(search.toUpperCase()),
          ) || []
        }
        search={search}
        // loading={loading}
        renderItem={(item) => (
          <CustomList.Item key={item.slug}>
            <CustomList.Item.Meta
              avatar={<Avatar className="avt-name" icon={<PhoneOutlined />} />}
              title={
                <Link href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.name}
                </Link>
              }
              description={
                item.access_level ? (
                  <span className="custom-list-text">
                    {t("accessLevel")}:
                    <Tooltip title={t(item.access_level)}>
                      <span className="access-level-icon">
                        {ACCESS_LEVEL_ICON[item.access_level]}
                      </span>
                    </Tooltip>
                  </span>
                ) : null
              }
            />
          </CustomList.Item>
        )}
      />
    </Widget>
  );
}

export default Meet;
