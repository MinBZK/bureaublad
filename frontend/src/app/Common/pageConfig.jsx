import DynamicIcon from "./DynamicIcon";

export const menuItem = (sideBarLinks) => [
  {
    key: "1",
    label: "Homepagina",
    icon: <DynamicIcon name={"HomeOutlined"} />,
  },
  {
    type: "divider",
  },
  {
    key: "grp",
    label: "Mijn Favoriete Apps",
    type: "group",
    children: sideBarLinks?.map((value) => ({
      key: value?.title,
      label: value?.title,
      icon: <DynamicIcon name={value?.icon} />,
    })),
  },
];
