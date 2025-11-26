"use client";

import { Avatar, List } from "antd";
import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import moment from "moment";
import { useState } from "react";

// Conversation
function Conversations({ title = "AI gesprek" }) {
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const {
    data: conv,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/conversations/chats", {
    page,
    page_size: 3,
    title: search,
  });

  return (
    <Widget
      title={title}
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
      page={page}
      setPage={setPage}
      total={conv?.count}
    >
      <List
        className="widget-list"
        dataSource={conv?.results || []}
        loading={loading}
        renderItem={(item) => (
          <List.Item key={item.id}>
            <List.Item.Meta
              title={<Link href={item?.url}>{item.title}</Link>}
              description={
                <span>
                  Laatste wijziging:{" "}
                  {moment(item.updated_at)?.format("DD-mm-YYYY HH:mm")}
                </span>
              }
            />
            <Link href={item?.url}>
              <Avatar className="avt-ai" icon={<WechatOutlined />} />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Conversations;
