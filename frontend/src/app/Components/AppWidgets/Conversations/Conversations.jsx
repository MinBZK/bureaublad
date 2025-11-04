"use client";
import React from "react";

import { Avatar, List } from "antd";
import { WechatOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import moment from "moment";

// Conversation
function Conversations() {
  const {
    data: conv,
    loading,
    error,
    refetch,
  } = useFetchWithRefresh("/api/v1/conversations/chats", { page: 1 });
  return (
    <Widget title="Gesprekken" error={error} onRefresh={refetch}>
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
                    Gemaakt op:
                    {moment(item.created_at)?.format("DD-mm-YYYY HH:mm")}
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
