"use client";
import { Layout, Menu } from "antd";
import { menuItem } from "../../../Common/pageConfig";

const { Sider } = Layout;

// TODO this component is currently not used. Consider integrating or removing it.
function SiderLayout({ items, collapsed }) {
  return (
    <Sider width={250} className="sider" collapsed={collapsed} trigger={null}>
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

// export const menuItem = (sideBarLinks) => [
//   {
//     key: "1",
//     label: "Home",
//     icon: <DynamicIcon name={"HomeOutlined"} />,
//   },
//   {
//     type: "divider",
//   },
//   {
//     key: "grp",
//     label: "Apps",
//     type: "group",
//     children: sideBarLinks?.map((value) => ({
//       key: value?.title,
//       label: value?.title,
//       icon: <DynamicIcon name={value?.icon} />,
//     })),
//   },
// ];
