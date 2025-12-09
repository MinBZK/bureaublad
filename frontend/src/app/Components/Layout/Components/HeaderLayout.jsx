"use client";
import { Affix, Avatar, Dropdown, Flex, Layout, Menu } from "antd";
import { LogoutOutlined, UserOutlined } from "@ant-design/icons";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { menuItem } from "../../../Common/pageConfig";
import AiAssistant from "../../AppWidgets/AiAssistant/AiAssistant";

const { Header } = Layout;

function HeaderLayout({ isProfile = true, profile, applications }) {
  const pathname = usePathname();

  // Determine selected key based on current path
  const getSelectedKey = () => {
    if (pathname === "/") return ["home"];
    const pathSegment = pathname.slice(1); // Remove leading slash
    return [pathSegment];
  };

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
    <Affix>
      <Header>
        <Flex>
          <div className="logo">
            <span className="logo-txt">Mijn Bureau</span>
          </div>
          {applications && (
            <Menu
              theme="dark"
              mode="horizontal"
              selectedKeys={getSelectedKey()}
              items={menuItem(applications)}
              className="header-menu"
            />
          )}
          {applications?.some(
            (value) => value?.id === "ai" && value?.enabled,
          ) && <AiAssistant />}
          {!isProfile && (
            <Dropdown menu={{ items }}>
              <Link className="profile-link" href="/#">
                <Avatar icon={<UserOutlined />} /> {profile}
              </Link>
            </Dropdown>
          )}
        </Flex>
      </Header>
    </Affix>
  );
}

export default HeaderLayout;
