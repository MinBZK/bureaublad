"use client";
import React from "react";
import { Avatar, Divider, Flex, Typography } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { Layout, Menu, theme, Input } from "antd";
import Link from "next/link";
import { menuItem } from "../Common/pageConfig";
import Image from "next/image";

const { Header, Content, Sider } = Layout;
const { Search } = Input;

export default function PageLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  return (
    <Layout>
      <Header>
        <Flex justify={"space-between"}>
          <div>
            {/* <span style={{ color: "white" }}>Mijn Bureau</span> */}
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
      <Layout>
        <Sider width={250} style={{ background: colorBgContainer }}>
          <Search
            placeholder="Zoeken"
            // onSearch={onSearch}
            style={{ width: "100%", padding: 10 }}
          />

          <Menu
            mode="inline"
            defaultSelectedKeys={["1"]}
            defaultOpenKeys={["sub1"]}
            style={{ height: "100%", borderInlineEnd: 0 }}
            items={menuItem}
          />
        </Sider>
        <Layout style={{ padding: "0 24px 24px" }}>
          <Content
            style={{
              padding: 24,
              margin: 0,
              height: "100vh",
              background: "#f5f5f5",
              borderRadius: borderRadiusLG,
            }}
          >
            <Typography.Title>Goedemiddag Berry</Typography.Title>
            <Divider/>
            {children}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
}

export function valueOrEmptyString(
  textContent: string | null | undefined
): string {
  if (textContent) {
    return textContent;
  }
  return "";
}
