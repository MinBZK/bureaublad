import Link from "next/link";
import DynamicIcon from "./DynamicIcon";

export const menuItem = (sideBarLinks) => [
  {
    key: 0,
    label: <Link href={"/"}>{"Home"}</Link>,
    icon: <DynamicIcon name={"HomeOutlined"} />,
  },

  ...sideBarLinks?.map((value, index) => ({
    key: index + 1,
    label: (
      <Link href={value?.url} rel="noopener noreferrer" target="_blank">
        {value?.title}
      </Link>
    ),
    icon: <DynamicIcon name={value?.icon} />,
  })),
];
