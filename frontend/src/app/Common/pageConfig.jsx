import DynamicIcon from "./DynamicIcon";

export const menuItem = (sideBarLinks) => [
  {
    key: 0,
    label: "Home",
    icon: <DynamicIcon name={"HomeOutlined"} />,
  },

  ...sideBarLinks?.map((value, index) => ({
    key: index + 1,
    label: value?.title,
    icon: <DynamicIcon name={value?.icon} />,
  })),
];
