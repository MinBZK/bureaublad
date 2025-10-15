"use client";
import React from "react";
import { Avatar, Dropdown, Flex, Layout } from "antd";
import { LogoutOutlined, UserOutlined } from "@ant-design/icons";
import Link from "next/link";
import Image from "next/image";
import { baseUrl } from "@/app/Common/pageConfig";

const { Header } = Layout;

function HeaderLayout({ isProfile = true }) {
  const items = [
    {
      key: "1",
      label: <Link href={`/profile`}>Profiel</Link>,
      icon: <UserOutlined />,
    },
    {
      key: "2",
      label: <Link href={`${baseUrl}/api/v1/auth/logout`}>Uitloggen</Link>,
      icon: <LogoutOutlined />,
      danger: true,
    },
  ];
  return (
    <Header>
      <Flex justify={"space-between"}>
        <div>
          <Image
            src="/mijnbureau.svg"
            alt="logo"
            width="50"
            height="50"
            style={{ marginTop: 5 }}
          />
          <span style={{ color: "white" }}>Mijn Bureau</span>
        </div>
        {!isProfile && (
          <Dropdown menu={{ items }}>
            <Link href="/#">
              <Avatar icon={<UserOutlined />} />
            </Link>
          </Dropdown>
        )}
      </Flex>
    </Header>
  );
}

export default HeaderLayout;
