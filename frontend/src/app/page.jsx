"use client";
import React from "react";
import { Col, Row, Card, Calendar, theme } from "antd";
import Files from "./Components/AppWidgets/Files/Files";
import Chat from "./Components/AppWidgets/Chat/Chat";
import Note from "./Components/AppWidgets/Notes/Notes";
import VideoChat from "./Components/AppWidgets/VideoChat/VideoChat";
// import Email from "./features/Email/Email";
import Drive from "./Components/AppWidgets/Drive/Drive";
import { useAppContext } from "./Components/Context/AppContext";
// import DynamicIcon from "./Common/DynamicIcon";
import AiAssistant from "./Components/AppWidgets/AiAssistant/AiAssistant";

export default function Home() {
  const { items } = useAppContext();
  const { token } = theme.useToken();
  const wrapperStyle = {
    width: 300,
    border: `1px solid ${token.colorBorderSecondary}`,
    borderRadius: token.borderRadiusLG,
  };

  return (
    <React.Fragment>
      {items?.cards?.ai && <AiAssistant />}
      <Row gutter={16} className="space-up">
        <Col span={8}>{items?.cards?.docs && <Note />}</Col>
        <Col span={8}>{items?.cards?.drive && <Drive />}</Col>
        <Col span={8}>{items?.cards?.ocs && <Files />}</Col>
      </Row>
      <Row gutter={16} className="space-up">
        <Col span={8}>
          {items?.cards?.conversation && <Chat />}

          {/* <Email /> */}
        </Col>
        <Col span={8}>{items?.cards?.meet && <VideoChat />}</Col>
        <Col span={8}>
          {items?.cards?.calendar && (
            <Card title="Agenda" variant="borderless">
              <div style={wrapperStyle}>
                <Calendar fullscreen={false} onPanelChange={undefined} />
              </div>
            </Card>
          )}
        </Col>
      </Row>
    </React.Fragment>
  );
}
