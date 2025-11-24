"use client";
import React from "react";
import { List } from "antd";
import Files from "./Components/AppWidgets/Files/Files";
import Chat from "./Components/AppWidgets/Conversations/Conversations";
import Note from "./Components/AppWidgets/Notes/Notes";
import VideoChat from "./Components/AppWidgets/VideoChat/VideoChat";
import Drive from "./Components/AppWidgets/Drive/Drive";
import { useAppContext } from "./Components/Context/AppContext";
import AiAssistant from "./Components/AppWidgets/AiAssistant/AiAssistant";
import Sheets from "./Components/AppWidgets/Sheets/Sheets";

export default function Home() {
  const { items } = useAppContext();
  const components = [
    items?.cards?.docs && <Note key="docs" />,
    items?.cards?.drive && <Drive key="drive" />,
    items?.cards?.ocs && <Files key="ocs" />,
    items?.cards?.grist && <Sheets key="sheet" />,
    items?.cards?.conversation && <Chat key="conversation" />,
    items?.cards?.meet && <VideoChat key="meet" />,
  ].filter(Boolean);

  return (
    <React.Fragment>
      {items?.cards?.ai && <AiAssistant key="ai" />}
      <List
        className="dashboard-list"
        grid={{ gutter: 16, xs: 1, sm: 1, md: 2, lg: 2, xl: 3, xxl: 3 }}
        dataSource={components}
        renderItem={(item) => <List.Item>{item}</List.Item>}
      />
    </React.Fragment>
  );
}
