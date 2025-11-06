"use client";
import React, { useState } from "react";
import { Avatar, List } from "antd";
import { EditOutlined, FileOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import moment from "moment";

// NextCloud
function Files() {
  const [searchTerm, setSearchTerm] = useState("");
  const {
    data: files,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh(
    searchTerm ? "/api/v1/ocs/search" : "/api/v1/ocs/activities",
    searchTerm ? { term: searchTerm } : {},
  );

  const onSearch = (value) => {
    setSearchTerm(value);
  };
  return (
    <Widget
      title="Bestanden"
      setSearch={onSearch}
      error={error}
      onRefresh={onRefresh}
    >
      <List
        dataSource={files}
        loading={loading}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.datetime}>
              <List.Item.Meta
                avatar={<Avatar icon={<FileOutlined />} className="avt-doc" />}
                title={<Link href={item?.url}>{item.object_filename}</Link>}
                description={
                  <span>
                    Laatste wijziging:{" "}
                    {moment(item.datetime)?.format("DD-mm-YYYY HH:mm")}
                  </span>
                }
              />
              <Link href="/#">
                <EditOutlined />
              </Link>
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default Files;
