"use client";
import React from "react";

import { Layout, Menu, Input } from "antd";
import { menuItem } from "../../Common/pageConfig";
const { Search } = Input;
const { Sider } = Layout;

function SiderLayout({ items, colorBgContainer }) {
  return (
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
        items={items && menuItem(items?.sidebar_links)}
      />
    </Sider>
  );
}

export default SiderLayout;
