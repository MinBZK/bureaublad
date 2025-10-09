"use client";
import React, { useState, useEffect } from "react";
import { Card, Result } from "antd";
import { Avatar, List } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import { baseUrl } from "@/app/Common/pageConfig";
import axios from "axios";

function Docs() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  
  useEffect(() => {
    setLoading(true);

    const fetchDocs = async () => {
      try {
        const res = await axios.get(baseUrl + "/api/v1/docs/documents");
        setDocs(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDocs();
  }, []);

  return (
    <Card title="Docs" variant="borderless" loading={loading}>
      {error ? (
        <Result status="warning" title={error} style={{marginTop: "-10%"}}/>
      ) : (
        <List
          dataSource={docs}
          renderItem={(item) => (
            <List.Item key={item.description}>
              <List.Item.Meta
                avatar={<Avatar icon={<FileTextOutlined />} />}
                title={<Link href={item?.url}>{item.title}</Link>}
                description={`Geüpdatet: ${item.updated_date}`}
              />
              <Link href={item?.url}>
                <EditOutlined />
              </Link>
            </List.Item>
          )}
        />
      )}
    </Card>
  );
}

export default Docs;
