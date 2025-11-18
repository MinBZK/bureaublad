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
  const [page, setPage] = useState(1);
  const {
    data: meet,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/meet/rooms", { page: 1, title: search });

  return (
    <Widget
      title="Videoconferentie"
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
      page={page}
      setPage={setPage}
      total={meet?.count || 0}
    >
      <List
        dataSource={meet?.results || []}
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
                description={<span>Pincode: {item.pin_code}</span>}
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
