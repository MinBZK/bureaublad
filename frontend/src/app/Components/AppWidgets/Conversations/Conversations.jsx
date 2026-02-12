"use client";

import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import moment from "moment";
import { useState } from "react";
import { useTranslations } from "@/i18n/TranslationsProvider";
import CustomList from "@/app/Common/CustomList";

// Conversation
function Conversations({ app }) {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const t = useTranslations("Conversations");
  const {
    data: conv,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/conversations/chats", {
    page,
    page_size: 3,
    title: search,
  });

  return (
    <Widget
      title={t("title")}
      app={app}
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
      page={page}
      setPage={setPage}
      total={conv?.count}
    >
      <CustomList
        className="widget-list"
        dataSource={conv?.results || []}
        loading={loading}
        renderItem={(item) => (
          <CustomList.Item key={item.id}>
            <CustomList.Item.Meta
              title={
                <Link
                  href={item?.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item.title}
                </Link>
              }
              description={
                <span>
                  {t("lastModified")} :
                  {moment.utc(item.updated_at)?.format("DD-MM-YYYY HH:mm")}
                </span>
              }
            />
            <Link href={item?.url} target="_blank" rel="noopener noreferrer">
              <WechatOutlined className="widget-icon-primary" />
            </Link>
          </CustomList.Item>
        )}
      />
    </Widget>
  );
}

export default Conversations;
