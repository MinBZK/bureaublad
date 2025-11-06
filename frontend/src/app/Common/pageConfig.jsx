import DynamicIcon from "./DynamicIcon";

export const menuItem = (sideBarLinks) => [
  {
    key: "1",
    label: "Home",
    icon: <DynamicIcon name={"HomeOutlined"} />,
  },
  {
    type: "divider",
  },
  {
    key: "grp",
    label: "Favoriete Apps",
    type: "group",
    children: sideBarLinks?.map((value) => ({
      key: value?.title,
      label: value?.title,
      icon: <DynamicIcon name={value?.icon} />,
    })),
  },
];
