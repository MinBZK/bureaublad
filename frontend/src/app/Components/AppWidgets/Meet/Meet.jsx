"use client";
import { useState } from "react";
import { Avatar, List } from "antd";
import { PhoneOutlined } from "@ant-design/icons";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import Link from "next/link";

// meet
function Meet({ title = "Videoconferentie" }) {
  // TODO search functionality is implemented in the frontend only because Meet dose not support search
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const {
    data: meet,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh("/api/v1/meet/rooms", { page, page_size: 3 });

  return (
    <Widget
      title={title}
      error={error}
      onRefresh={onRefresh}
      setSearch={setSearch}
      page={page}
      setPage={setPage}
      total={meet?.count || 0}
    >
      <List
        dataSource={
          meet?.results?.filter((value) =>
            value?.name?.toUpperCase()?.includes(search.toUpperCase()),
          ) || []
        }
        loading={loading}
        renderItem={(item) => (
          <List.Item key={item.slug}>
            <List.Item.Meta
              avatar={
                <Avatar className="avt-name">
                  {item?.name?.at(0)?.toUpperCase()}
                </Avatar>
              }
              title={<Link href={item.url}>{item.name}</Link>}
              description={
                item.pin_code ? <span>Pincode: {item.pin_code}</span> : null
              }
            />
            <Link href={item.url}>
              <Avatar className="avt-call" icon={<PhoneOutlined />} />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Meet;
