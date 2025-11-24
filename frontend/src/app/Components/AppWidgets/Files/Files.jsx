"use client";
import React, { useState } from "react";
import { Avatar, Button, Divider, Flex, List } from "antd";
import {
  EditOutlined,
  FileOutlined,
  LeftOutlined,
  RightOutlined,
} from "@ant-design/icons";
import Link from "next/link";
import Widget from "@/app/Common/Widget";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import moment from "moment";

// NextCloud
function Files() {
  const [searchTerm, setSearchTerm] = useState("");
  const [since, setSince] = useState(null);
  const [sinceHistory, setSinceHistory] = useState([]); // Stack to track previous 'since' values
  const limit = 3;

  const {
    data: files,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh(
    searchTerm ? "/api/v1/ocs/search" : "/api/v1/ocs/activities",
    searchTerm
      ? { term: searchTerm, limit }
      : since
        ? { since, limit }
        : { limit },
  );

  const onSearch = (value) => {
    setSearchTerm(value);
    setSince(null); // Reset pagination when searching
    setSinceHistory([]); // Clear history when searching
  };

  // Extract the last activity_id from files to use for next pagination
  const getNextSince = () => {
    if (files && files.length > 0) {
      const lastFile = files[files.length - 1];
      return lastFile.activity_id;
    }
    return null;
  };

  const handlePageChange = (direction) => {
    if (direction === "next") {
      const nextSince = getNextSince();
      // Only move forward if we have a new 'since' value different from current
      if (nextSince && nextSince !== since) {
        // Push current 'since' to history before moving forward
        setSinceHistory((prev) => [...prev, since]);
        setSince(nextSince);
      }
    } else if (direction === "prev") {
      // Pop the last 'since' from history to go back
      if (sinceHistory.length > 0) {
        const previousSince = sinceHistory[sinceHistory.length - 1];
        setSinceHistory((prev) => prev.slice(0, -1)); // Remove last item from history
        setSince(previousSince);
      }
    }
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
        className="widget-list"
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
      <Divider />
      <Flex justify="end">
        <Button
          color="primary"
          variant="text"
          onClick={() => handlePageChange("prev")}
          disabled={sinceHistory.length === 0}
        >
          <LeftOutlined />
        </Button>
        <Button
          color="primary"
          variant="text"
          onClick={() => handlePageChange("next")}
          disabled={
            !files ||
            files.length === 0 ||
            files.length < limit ||
            getNextSince() === since
          }
        >
          <RightOutlined />
        </Button>
      </Flex>
    </Widget>
  );
}

export default Files;
