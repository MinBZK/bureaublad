"use client";
import React, { useState } from "react";
import { Avatar, Button, Divider, Flex } from "antd";
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
import { useTranslations } from "@/i18n/TranslationsProvider";
import CustomList from "@/app/Common/CustomList";

// NextCloud
function Files({ title = "Bestanden" }) {
  const [searchTerm, setSearchTerm] = useState("");
  const [since, setSince] = useState(null);
  const [sinceHistory, setSinceHistory] = useState([]); // Stack to track previous 'since' values
  const t = useTranslations("Files");
  const limit = 3;

  const {
    data: files,
    loading,
    error,
    onRefresh,
  } = useFetchWithRefresh(
    searchTerm ? "/ocs/search" : "/ocs/activities",
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
      title={title}
      setSearch={onSearch}
      error={error}
      onRefresh={onRefresh}
    >
      <CustomList
        dataSource={files}
        loading={loading}
        className="widget-list"
        renderItem={(item) => (
          <CustomList.Item key={item.activity_id}>
            <CustomList.Item.Meta
              avatar={<Avatar icon={<FileOutlined />} className="avt-doc" />}
              title={
                <Link
                  href={item?.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item.object_filename}
                </Link>
              }
              description={
                <span>
                  {t("lastModified")}:
                  {moment(item.datetime)?.format("DD-mm-YYYY HH:mm")}
                </span>
              }
            />
            <Link href={item?.url} target="_blank" rel="noopener noreferrer">
              <EditOutlined />
            </Link>
          </CustomList.Item>
        )}
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
