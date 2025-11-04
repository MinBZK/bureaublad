"use client";
import { useState } from "react";
import { Avatar, List } from "antd";
import { PhoneOutlined } from "@ant-design/icons";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import Link from "next/link";

// meet
function VideoChat() {
  // TODO search functionality is not implemented in the backend yet
  const [search, setSearch] = useState("");
  const {
    data: meet,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/meet/rooms", { page: 1, title: search });
  return (
    <Widget
      title="Video Chat"
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
    >
      <List
        dataSource={meet}
        loading={loading}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.slug}>
              <List.Item.Meta
                avatar={
                  <Avatar className="avt-name">
                    {item?.name?.at(0)?.toUpperCase()}
                  </Avatar>
                }
                title={<Link href={item.url}>{item.name}</Link>}
                description={<span>Hostsleutel:{item.pin_code}</span>}
              />
              <Link href={item.url}>
                <Avatar className="avt-call" icon={<PhoneOutlined />} />
              </Link>
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default VideoChat;
