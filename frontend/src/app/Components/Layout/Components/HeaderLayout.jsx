"use client";
import React from "react";
import { Avatar, Flex, Layout } from "antd";
import { UserOutlined } from "@ant-design/icons";
import Link from "next/link";
import Image from "next/image";

const { Header } = Layout;

function HeaderLayout() {
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
        <div>
          <Link href="/#">
            <Avatar icon={<UserOutlined />} />
          </Link>
        </div>
      </Flex>
    </Header>
  );
}

export default HeaderLayout;
