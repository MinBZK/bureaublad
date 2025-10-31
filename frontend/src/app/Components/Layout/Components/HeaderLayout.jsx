"use client";
import React from "react";
import { Avatar, Dropdown, Flex, Layout } from "antd";
import { LogoutOutlined, UserOutlined } from "@ant-design/icons";
import Link from "next/link";
import Image from "next/image";
import SearchFiles from "../../../Common/SearchFiles";

const { Header } = Layout;

function HeaderLayout({ isProfile = true, profile }) {
  const items = [
    {
      key: "1",
      label: profile,
      icon: <UserOutlined />,
    },
    {
      key: "2",
      label: <Link href={`/api/v1/auth/logout`}>Uitloggen</Link>,
      icon: <LogoutOutlined />,
      danger: true,
    },
  ];
  return (
    <Header>
      <Flex justify={"space-between"}>
        <div>
          <span className="logo-txt">Mijn Bureau</span>
        </div>

        <SearchFiles className="header-search" />
        {!isProfile && (
          <Dropdown menu={{ items }}>
            <Link className="profile-link" href="/#">
              <Avatar icon={<UserOutlined />} /> {profile}
            </Link>
          </Dropdown>
        )}
      </Flex>
    </Header>
  );
}

export default HeaderLayout;
