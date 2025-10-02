import {
  CalendarOutlined,
  FileOutlined,
  FileTextOutlined,
  HomeOutlined,
  LaptopOutlined,
  MailOutlined,
  NotificationOutlined,
  UserOutlined,
  VideoCameraOutlined,
  WechatOutlined,
} from "@ant-design/icons";
import type { MenuProps } from "antd";

export const menuItem: MenuProps["items"] = [
  {
    key: "1",
    label: "Homepagina",
    icon: <HomeOutlined />,
  },
  {
    type: "divider",
  },
  {
    key: "grp",
    label: "Mijn Favoriete Apps",
    type: "group",
    children: [
      {
        key: "office",
        label: "Office",
        icon: <FileOutlined />,
      },
      {
        key: "chat",
        label: "Chat",
        icon: <WechatOutlined />,
      },
      {
        key: "docs",
        label: "Docs",
        icon: <FileTextOutlined />,
      },
      {
        key: "Email",
        label: "Email",
        icon: <MailOutlined />,
      },
      {
        key: "meeting",
        label: "Meeting",
        icon: <VideoCameraOutlined />,
      },
      {
        key: "calendar",
        label: "Calendar",
        icon: <CalendarOutlined />,
      },
    ],
  },
];

export function valueOrEmptyString(
  textContent: string | null | undefined
): string {
  if (textContent) {
    return textContent;
  }
  return "";
}
