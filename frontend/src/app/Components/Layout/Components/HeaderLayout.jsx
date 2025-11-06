"use client";
import { Avatar, Dropdown, Flex, Layout, Menu } from "antd";
import { LogoutOutlined, UserOutlined } from "@ant-design/icons";
import Link from "next/link";
import { menuItem } from "../../../Common/pageConfig";

const { Header } = Layout;

function HeaderLayout({ isProfile = true, profile, applications }) {
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
      <Flex>
        <div className="logo">
          <span className="logo-txt">Mijn Bureau</span>
        </div>
        {applications && (
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={["0"]}
            items={menuItem(applications)}
            style={{ flex: 1, minWidth: 0 }}
          />
        )}
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
