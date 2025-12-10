"use client";
import { List } from "antd";
import { useAppContext } from "./Components/Context/AppContext";
import { availableWidgetComponents } from "./Common/pageConfig";

export default function Home() {
  const { appConfig } = useAppContext();

  const appComponents = availableWidgetComponents(
    appConfig?.applications || [],
  );

  return (
    <List
      className="dashboard-list"
      grid={{ gutter: 16, xs: 1, sm: 1, md: 1, lg: 2, xl: 2, xxl: 3 }}
      dataSource={appComponents}
      renderItem={(item) => <List.Item>{item}</List.Item>}
    />
  );
}
