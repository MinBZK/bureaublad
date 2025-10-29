"use client";
import { Layout, Menu } from "antd";
import { menuItem } from "../../../Common/pageConfig";

const { Sider } = Layout;

function SiderLayout({ items }) {
  return (
    <Sider width={250} className="sider">
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
