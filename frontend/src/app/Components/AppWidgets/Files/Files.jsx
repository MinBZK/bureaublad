"use client";
import React, { useEffect, useState } from "react";
import { Avatar, List } from "antd";
import { EditOutlined, FileOutlined } from "@ant-design/icons";
import Link from "next/link";
import axios from "axios";
import Widget from "@/app/Common/Widget";
import moment from "moment";

// NextCloud
function Files() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    const fetchDocs = async () => {
      try {
        const res = await axios.get("/api/v1/ocs/activities");
        setFiles(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, []);

  const onSearch = async (value) => {
    try {
      const res = await axios.get(`/api/v1/ocs/search?term=${value}`);
      setFiles(res.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  return (
    <Widget
      title="Bestanden"
      setSearch={onSearch}
      loading={loading}
      error={error}
    >
      <List
        dataSource={files}
        renderItem={(item) => (
          <List.Item key={item.datetime}>
            <List.Item.Meta
              avatar={<Avatar icon={<FileOutlined />} className="avt-doc" />}
              title={<Link href={item?.url}>{item.object_filename}</Link>}
              description={
                <span>
                  Gemaakt op:
                  {moment(item.datetime)?.format("DD-mm-YYYY HH:mm")}
                </span>
              }
            />
            <Link href="/#">
              <EditOutlined />
            </Link>
          </List.Item>
        )}
      />
    </Widget>
  );
}

export default Files;
