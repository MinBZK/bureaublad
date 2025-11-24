"use client";
import React from "react";
import { List } from "antd";
import Files from "./Components/AppWidgets/Files/Files";
import Conversations from "./Components/AppWidgets/Conversations/Conversations";
import Documents from "./Components/AppWidgets/Documents/Documents";
import Meet from "./Components/AppWidgets/Meet/Meet";
import Drive from "./Components/AppWidgets/Drive/Drive";
import { useAppContext } from "./Components/Context/AppContext";
import AiAssistant from "./Components/AppWidgets/AiAssistant/AiAssistant";
import Sheets from "./Components/AppWidgets/Sheets/Sheets";

export default function Home() {
  const { items } = useAppContext();
  const components = [
    items?.cards?.docs && <Documents key="docs" />,
    items?.cards?.drive && <Drive key="drive" />,
    items?.cards?.ocs && <Files key="ocs" />,
    items?.cards?.grist && <Sheets key="sheet" />,
    items?.cards?.conversation && <Conversations key="conversation" />,
    items?.cards?.meet && <Meet key="meet" />,
  ].filter(Boolean);

  return (
    <React.Fragment>
      {items?.cards?.ai && <AiAssistant key="ai" />}
      <List
        className="dashboard-list"
        grid={{ gutter: 16, xs: 1, sm: 1, md: 1, lg: 2, xl: 2, xxl: 3 }}
        dataSource={components}
        renderItem={(item) => <List.Item>{item}</List.Item>}
      />
    </React.Fragment>
  );
}
