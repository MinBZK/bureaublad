"use client";
import { Affix, Avatar, Dropdown, Flex, Layout, Menu } from "antd";
import {
  LogoutOutlined,
  UserOutlined,
  GlobalOutlined,
  BgColorsOutlined,
} from "@ant-design/icons";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { menuItem } from "../../../Common/pageConfig";
import AiAssistant from "../../AppWidgets/AiAssistant/AiAssistant";
import { useTranslations } from "../../../../i18n/TranslationsProvider";
import { useLanguage } from "../../../../i18n/LanguageContext";
import { useTheme } from "../../Context/ThemeContext";
const { Header } = Layout;

function HeaderLayout({ isProfile = true, profile, applications }) {
  const pathname = usePathname();
  const tHome = useTranslations("HomePage");
  const tHeader = useTranslations("Header");
  const tNav = useTranslations("Navigation");
  const tTheme = useTranslations("Theme");
  const { locale, setLocale } = useLanguage();
  const { theme, toggleTheme } = useTheme();

  // Determine selected key based on current path
  const getSelectedKey = () => {
    if (pathname === "/") return ["home"];
    const pathSegment = pathname.slice(1); // Remove leading slash
    return [pathSegment];
  };

  const handleLanguageChange = () => {
    const newLocale = locale === "nl" ? "en" : "nl";
    setLocale(newLocale);
  };

  const items = [
    {
      key: "1",
      label: (
        <span onClick={handleLanguageChange}>
          {locale === "nl"
            ? tHeader("languageEnglish")
            : tHeader("languageDutch")}
        </span>
      ),
      icon: <GlobalOutlined />,
    },
    {
      key: "2",
      label: (
        <span onClick={toggleTheme}>
          {theme === "light" ? tTheme("dark") : tTheme("light")}
        </span>
      ),
      icon: <BgColorsOutlined />,
    },
    {
      key: "3",
      label: <Link href={`/api/v1/auth/logout`}>{tHome("logout")}</Link>,
      icon: <LogoutOutlined />,
      danger: true,
    },
  ];

  return (
    <Affix>
      <Header>
        <Flex>
          <div className="logo">
            <Link className="logo-txt" href="/">
              {tHome("title")}
            </Link>
          </div>
          {applications && (
            <Menu
              theme="dark"
              mode="horizontal"
              selectedKeys={getSelectedKey()}
              items={menuItem(applications, tNav)}
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
