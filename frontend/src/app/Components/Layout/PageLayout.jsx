"use client";
import React from "react";
import { Divider, Typography, Layout, theme } from "antd";
import SiderLayout from "./Components/SiderLayout";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../../Context/AppContext";
const { Content } = Layout;

export default function PageLayout({ children }) {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const { items } = useAppContext();

  return (
    <Layout>
      <HeaderLayout />
      <Layout>
        <SiderLayout colorBgContainer={colorBgContainer} items={items} />
        <Layout style={{ padding: "0 24px 24px" }}>
          <Content
            style={{
              padding: 24,
              margin: 0,
              // height: "100vh",
              background: "#f5f5f5",
              borderRadius: borderRadiusLG,
            }}
          >
            <Typography.Title>Goedemiddag</Typography.Title>
            <Divider />
            {children}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
}
