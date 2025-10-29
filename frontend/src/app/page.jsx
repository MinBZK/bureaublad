"use client";
import React from "react";
import { Col, Row } from "antd";
import Files from "./Components/AppWidgets/Files/Files";
import Chat from "./Components/AppWidgets/Conversations/Conversations";
import Note from "./Components/AppWidgets/Notes/Notes";
import VideoChat from "./Components/AppWidgets/VideoChat/VideoChat";
import Drive from "./Components/AppWidgets/Drive/Drive";
import { useAppContext } from "./Components/Context/AppContext";
import AiAssistant from "./Components/AppWidgets/AiAssistant/AiAssistant";

export default function Home() {
  const { items } = useAppContext();
  const components = [
    items?.cards?.docs && <Note key="docs" />,
    items?.cards?.drive && <Drive key="drive" />,
    items?.cards?.ocs && <Files key="ocs" />,
    items?.cards?.conversation && <Chat key="conversation" />,
    items?.cards?.meet && <VideoChat key="meet" />,
    items?.cards?.ai && <AiAssistant key="ai" />,
  ].filter(Boolean);

  const rows = [];
  for (let i = 0; i < components.length; i += 3) {
    rows.push(components.slice(i, i + 3));
  }

  return (
    <React.Fragment>
      {rows.map((row, rowIndex) => (
        <Row gutter={16} className="space-up" key={rowIndex}>
          {row.map((Component, colIndex) => (
            <Col span={8} key={colIndex}>
              {Component}
            </Col>
          ))}
        </Row>
      ))}
    </React.Fragment>
  );
}
