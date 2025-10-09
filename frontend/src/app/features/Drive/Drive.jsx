"use client";
import React, { useState, useEffect } from "react";
import { Card, Result } from "antd";
import { Avatar, List } from "antd";
import { EditOutlined } from "@ant-design/icons";
import Link from "next/link";
import { baseUrl } from "@/app/Common/pageConfig";
import moment from "moment";
import axios from "axios";

function Drive() {
  const [drive, setDrive] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setLoading(true);
    const fetchDocs = async () => {
      try {
        const res = await axios.get(baseUrl + "/api/v1/drive/documents");
        setDrive(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, []);

  console.log(drive);
  return (
    <Card title="Drive" variant="borderless" loading={loading}>
      {error ? (
        <Result status="warning" title={error} style={{ marginTop: "-10%" }} />
      ) : (
        <List
          dataSource={drive}
          renderItem={(item) => (
            <List.Item key={item.description}>
              <List.Item.Meta
                avatar={
                  <Avatar
                    style={{
                      backgroundColor: "#f56a00",
                      verticalAlign: "middle",
                    }}
                  >
                    {item?.creator?.full_name.at(0)}
                  </Avatar>
                }
                title={<Link href={item?.url || ""}>{item.title}</Link>}
                description={`Gemaakt:
                  ${moment(item.created_at).format("DD-MM-YYYY, mm:ss")}`}
              />
              <Link href="/#">
                <EditOutlined />
              </Link>
            </List.Item>
          )}
        />
      )}
    </Card>
  );
}

export default Drive;

const data = [
  {
    id: "ae5508b3-ee3b-4dfb-b9b5-3e2f2e7aad45",
    abilities: {
      accesses_manage: true,
      accesses_view: true,
      children_list: true,
      children_create: true,
      destroy: true,
      hard_delete: true,
      favorite: true,
      link_configuration: true,
      invite_owner: true,
      move: false,
      restore: true,
      retrieve: true,
      tree: true,
      media_auth: true,
      partial_update: true,
      update: true,
      upload_ended: true,
    },
    created_at: "2025-10-07T20:19:04.484150Z",
    creator: { full_name: "Berry", short_name: "Berry" },
    depth: 1,
    is_favorite: false,
    link_role: "reader",
    link_reach: "restricted",
    nb_accesses: 1,
    numchild: 1,
    numchild_folder: 0,
    path: "ae5508b3-ee3b-4dfb-b9b5-3e2f2e7aad45",
    title: "Workspace",
    updated_at: "2025-10-07T20:19:04.484162Z",
    user_roles: ["owner"],
    type: "folder",
    upload_state: null,
    url: null,
    filename: null,
    mimetype: null,
    main_workspace: true,
    size: null,
    description: null,
    deleted_at: null,
    hard_delete_at: null,
  },
  {
    id: "058dafa1-2fea-4744-b8e4-54eb1a808594",
    abilities: {
      accesses_manage: true,
      accesses_view: true,
      children_list: true,
      children_create: true,
      destroy: true,
      hard_delete: true,
      favorite: true,
      link_configuration: true,
      invite_owner: true,
      move: true,
      restore: true,
      retrieve: true,
      tree: true,
      media_auth: true,
      partial_update: true,
      update: true,
      upload_ended: true,
    },
    created_at: "2025-10-08T18:58:46.428708Z",
    creator: {
      full_name: "Berry",
      short_name: "Berry",
    },
    depth: 2,
    is_favorite: false,
    link_role: "reader",
    link_reach: "restricted",
    nb_accesses: 1,
    numchild: 0,
    numchild_folder: 0,
    path: "ae5508b3-ee3b-4dfb-b9b5-3e2f2e7aad45.058dafa1-2fea-4744-b8e4-54eb1a808594",
    title: "mijnbureau-startpage.png",
    updated_at: "2025-10-08T18:58:46.428720Z",
    user_roles: ["owner"],
    type: "file",
    upload_state: "uploaded",
    url: "https://drive.demo.eu/media/item/058dafa1-2fea-4744-b8e4-54eb1a808594/mijnbureau-startpage.png",
    filename: "mijnbureau-startpage.png",
    mimetype: "image/png",
    main_workspace: false,
    size: 189030,
    description: null,
    deleted_at: null,
    hard_delete_at: null,
  },
  {
    id: "275d6193-279e-4957-aeb0-081eef7df1a9",
    abilities: {
      accesses_manage: true,
      accesses_view: true,
      children_list: true,
      children_create: true,
      destroy: true,
      hard_delete: true,
      favorite: true,
      link_configuration: true,
      invite_owner: true,
      move: true,
      restore: true,
      retrieve: true,
      tree: true,
      media_auth: true,
      partial_update: true,
      update: true,
      upload_ended: true,
    },
    created_at: "2025-10-07T20:19:19.415476Z",
    creator: {
      full_name: "Berry",
      short_name: "Berry",
    },
    depth: 2,
    is_favorite: false,
    link_role: "reader",
    link_reach: "restricted",
    nb_accesses: 1,
    numchild: 0,
    numchild_folder: 0,
    path: "ae5508b3-ee3b-4dfb-b9b5-3e2f2e7aad45.275d6193-279e-4957-aeb0-081eef7df1a9",
    title: "Berry-small.jpeg",
    updated_at: "2025-10-07T20:19:19.415490Z",
    user_roles: ["owner"],
    type: "file",
    upload_state: "uploaded",
    url: "https://drive.demo.eu/media/item/275d6193-279e-4957-aeb0-081eef7df1a9/Berry-small.jpeg",
    filename: "Berry-small.jpeg",
    mimetype: "image/jpeg",
    main_workspace: false,
    size: 308981,
    description: null,
    deleted_at: null,
    hard_delete_at: null,
  },
];
