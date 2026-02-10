"use client";
import { useState } from "react";
import { Avatar, message } from "antd";
import { PhoneOutlined } from "@ant-design/icons";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import Link from "next/link";
import { useTranslations } from "@/i18n/TranslationsProvider";
import CustomList from "@/app/Common/CustomList";

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    message.success("Copied!");
  });
};

// meet
function Meet() {
  // TODO search functionality is implemented in the frontend only because Meet dose not support search
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const t = useTranslations("Meet");
  const {
    data: meet,
    error,
    onRefresh,
  } = useFetchWithRefresh("/meet/rooms", { page, page_size: 3 });

  return (
    <Widget
      title={t("title")}
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
      page={page}
      setPage={setPage}
      total={meet?.count || 0}
    >
      <CustomList
        dataSource={
          meet?.results?.filter((value) =>
            value?.name?.toUpperCase()?.includes(search.toUpperCase()),
          ) || []
        }
        // loading={loading}
        renderItem={(item) => (
          <CustomList.Item key={item.slug}>
            <CustomList.Item.Meta
              avatar={
                <Avatar className="avt-name">
                  {item?.name?.at(0)?.toUpperCase()}
                </Avatar>
              }
              title={
                <Link href={item.url} target="_blank" rel="noopener noreferrer">
                  {item.name}
                </Link>
              }
              description={
                item.pin_code ? (
                  <span
                    className="custom-list-text-copy"
                    onClick={() => copyToClipboard(item.pin_code)}
                  >
                    {t("pincode")} : {item.pin_code}
                  </span>
                ) : null
              }
            />
            <Link href={item.url} target="_blank" rel="noopener noreferrer">
              <Avatar className="avt-call" icon={<PhoneOutlined />} />
            </Link>
          </CustomList.Item>
        )}
      />
    </Widget>
  );
}

export default Meet;
