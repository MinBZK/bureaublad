"use client";
import React from "react";
import { Col, Row, Card, Calendar, theme } from "antd";
import Files from "./features/Files/Files";
import Chat from "./features/Chat/Chat";
import Note from "./features/Notes/Notes";
import VideoChat from "./features/VideoChat/VideoChat";
// import Email from "./features/Email/Email";
import Drive from "./features/Drive/Drive";
import { useAppContext } from "./Context/AppContext";
// import DynamicIcon from "./Common/DynamicIcon";
import AiAssistant from "../app/features/AiAssistant/AiAssistant";

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
      {items?.applications?.ai && <AiAssistant />}
      <Row gutter={16} style={{ marginTop: 10 }}>
        <Col span={8}>{items?.applications?.docs && <Note />}</Col>
        <Col span={8}>{items?.applications?.drive && <Drive />}</Col>
        <Col span={8}>
          <Files />
        </Col>
      </Row>
      <Row gutter={16} style={{ marginTop: 10 }}>
        <Col span={8}>
          {items?.applications?.meet && <Chat />}

          {/* <Email /> */}
        </Col>
        <Col span={8}>{items?.applications?.meet && <VideoChat />}</Col>
        <Col span={8}>
          {items?.applications?.calendar && (
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
