"use client";

import { Avatar, List } from "antd";
import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import moment from "moment";
import { useState } from "react";

// Conversation
function Conversations() {
  // TODO search functionality is not implemented in the backend yet
  const [search, setSearch] = useState("");
  const {
    data: conv,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/conversations/chats", {
    page: 1,
    title: search,
  });

  return (
    <Widget
      title="AI gesprek"
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
    >
      <List
        dataSource={conv}
        loading={loading}
        renderItem={(item, index) =>
          index <= 2 && (
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
                <Avatar
                  style={{ backgroundColor: "#1677ff" }}
                  icon={<WechatOutlined />}
                />
              </Link>
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default Conversations;
