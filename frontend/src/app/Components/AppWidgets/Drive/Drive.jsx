"use client";
import React, { useState, useEffect } from "react";
import { Avatar, List } from "antd";
import { FileImageOutlined } from "@ant-design/icons";
import Link from "next/link";
import moment from "moment";
import axios from "axios";
import Widget from "@/app/Common/Widget";

function Drive() {
  const [drive, setDrive] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [favorite, setFavorite] = useState(false);
  const [search, setSearch] = useState("");
  useEffect(() => {
    setLoading(true);
    const fetchDocs = async () => {
      try {
        const res = await axios.get("/api/v1/drive/documents");
        setDrive(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, [favorite, search]);

  return (
    <Widget
      title="Drive"
      favorite={favorite}
      setFavorite={setFavorite}
      setSearch={setSearch}
      loading={loading}
      error={error}
    >
      <List
        dataSource={drive}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.description}>
              <List.Item.Meta
                avatar={
                  <Avatar
                    icon={<FileImageOutlined />}
                    style={{ backgroundColor: "#f56a00" }}
                  />
                }
                title={<Link href={item?.url || ""}>{item.title}</Link>}
                description={`Gemaakt:
                  ${moment(item.created_at).format("DD-MM-YYYY, mm:ss")}`}
              />
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default Drive;
