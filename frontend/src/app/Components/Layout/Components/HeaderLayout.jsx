"use client";
import { Affix, Avatar, Dropdown, Flex, Layout, Popover } from "antd";
import {
  BgColorsOutlined,
  DownOutlined,
  GlobalOutlined,
  LogoutOutlined,
  MoonOutlined,
  ProfileOutlined,
  SunOutlined,
  UserOutlined,
} from "@ant-design/icons";
import Link from "next/link";
import { usePathname } from "next/navigation";
import ColorPicker from "./ColorPicker";
import { useTranslations } from "../../../../i18n/TranslationsProvider";
import { useLanguage } from "../../../../i18n/LanguageContext";
import { useTheme } from "../../Context/ThemeContext";
const { Header } = Layout;

function HeaderLayout({
  isAuthenticated = false,
  profile,
  redirectUrl,
  isAdmin = false,
}) {
  const pathname = usePathname();
  const tHome = useTranslations("HomePage");
  const tHeader = useTranslations("Header");
  const tNav = useTranslations("Navigation");
  const tTheme = useTranslations("Theme");
  const { locale, setLocale } = useLanguage();
  const { theme, toggleTheme, brand, setBrand, palettes } = useTheme();

  const handleLanguageChange = () => {
    setLocale(locale === "nl" ? "en" : "nl");
  };

  const accountItems = [
    {
      key: "account",
      label: (
        <a href={redirectUrl} rel="noopener noreferrer" target="_blank">
          {tHeader("myAccount")}
        </a>
      ),
      icon: <ProfileOutlined />,
    },
    {
      key: "language",
      label:
        locale === "nl" ? tHeader("languageEnglish") : tHeader("languageDutch"),
      icon: <GlobalOutlined />,
      onClick: handleLanguageChange,
    },
    {
      key: "theme",
      label: theme === "light" ? tTheme("dark") : tTheme("light"),
      icon: theme === "light" ? <MoonOutlined /> : <SunOutlined />,
      onClick: toggleTheme,
    },
    {
      key: "logout",
      label: <Link href={`/api/v1/auth/logout`}>{tHome("logout")}</Link>,
      icon: <LogoutOutlined />,
      danger: true,
    },
  ];

  const header = (
    <Header className="rh-header">
      <Flex
        align="center"
        className={
          isAuthenticated
            ? "rh-header-inner"
            : "rh-header-inner rh-header-inner--minimal"
        }
      >
        <Link className="rh-logo" href="/">
          <span className="rh-logo-mark" aria-hidden="true">
            MB
          </span>
          <span className="rh-logo-text">{tHome("title")}</span>
        </Link>

        {isAuthenticated && (
          <nav className="rh-nav" aria-label={tNav("mainNavigation")}>
            <Link
              href="/"
              aria-current={pathname === "/" ? "page" : undefined}
              className={
                pathname === "/" ? "rh-nav-link is-active" : "rh-nav-link"
              }
            >
              {tNav("home")}
            </Link>
            {isAdmin && (
              <Link
                href="/admin"
                aria-current={pathname === "/admin" ? "page" : undefined}
                className={
                  pathname === "/admin"
                    ? "rh-nav-link is-active"
                    : "rh-nav-link"
                }
              >
                {tNav("admin")}
              </Link>
            )}
          </nav>
        )}

        <div className="rh-header-actions">
          <Popover
            trigger="click"
            placement="bottomRight"
            arrow={false}
            content={
              <ColorPicker
                brand={brand}
                onSelect={setBrand}
                palettes={palettes}
              />
            }
          >
            <button
              type="button"
              className="rh-icon-button"
              aria-label={tTheme("colors")}
              title={tTheme("colors")}
            >
              <BgColorsOutlined />
            </button>
          </Popover>

          {isAuthenticated ? (
            <Dropdown menu={{ items: accountItems }} placement="bottomRight">
              <button type="button" className="rh-account-button">
                <Avatar size="small" icon={<UserOutlined />} />
                {profile && <span className="rh-account-name">{profile}</span>}
                <DownOutlined className="rh-account-caret" />
              </button>
            </Dropdown>
          ) : (
            <button
              type="button"
              className="rh-language-button"
              onClick={handleLanguageChange}
            >
              <GlobalOutlined />
              <span>
                {locale === "nl"
                  ? tHeader("languageEnglish")
                  : tHeader("languageDutch")}
              </span>
            </button>
          )}
        </div>
      </Flex>
    </Header>
  );

  return <Affix>{header}</Affix>;
}

export default HeaderLayout;
