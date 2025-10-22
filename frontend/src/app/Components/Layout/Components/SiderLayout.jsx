"use client";
import React from "react";

import { Layout, Menu, Input } from "antd";
import { menuItem } from "../../../Common/pageConfig";
const { Search } = Input;
const { Sider } = Layout;

function SiderLayout({ items }) {
  return (
    <Sider width={250} className="sider">
      <Search
        placeholder="Zoeken"
        // onSearch={onSearch}
        className="sider-search"
      />

      <Menu
        mode="inline"
        defaultSelectedKeys={["1"]}
        defaultOpenKeys={["sub1"]}
        items={items && menuItem(items?.applications)}
      />
    </Sider>
  );
}

export default SiderLayout;
