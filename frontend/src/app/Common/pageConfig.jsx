import Link from "next/link";
import DynamicIcon from "./DynamicIcon";
import Documents from "../Components/AppWidgets/Documents/Documents";
import Drive from "../Components/AppWidgets/Drive/Drive";
import Files from "../Components/AppWidgets/Files/Files";
import Sheets from "../Components/AppWidgets/Sheets/Sheets";
import Conversations from "../Components/AppWidgets/Conversations/Conversations";
import Meet from "../Components/AppWidgets/Meet/Meet";

export const menuItem = (applications, t) => [
  {
    key: "home",
    label: <Link href={"/"}>{t ? t("home") : "Home"}</Link>,
    icon: <DynamicIcon name={"HomeOutlined"} />,
  },

  ...applications
    ?.filter((app) => app?.url && app?.title)
    .map((app) => ({
      key: app.id,
      label: app.iframe ? (
        <Link href={`/${app.id}`}>{app.title}</Link>
      ) : (
        <Link href={app.url} rel="noopener noreferrer" target="_blank">
          {app.title}
        </Link>
      ),
      icon: <DynamicIcon name={app.icon} />,
    })),
];

export const availableWidgetComponents = (applications) => {
  const componentMap = {
    docs: Documents,
    drive: Drive,
    ocs: Files,
    grist: Sheets,
    conversation: Conversations,
    meet: Meet,
  };

  return applications
    .filter((app) => app.enabled)
    .map((app) => {
      const Component = componentMap[app.id];
      return Component ? <Component key={app.id} title={app?.title} /> : null;
    })
    .filter(Boolean);
};
