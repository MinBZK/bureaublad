"use client";
import React from "react";
import { Col, Row, Card, Calendar, theme } from "antd";
import Office from "./features/Office/Office";
import Chat from "./features/Chat/Chat";
import Docs from "./features/Docs/Docs";
import VideoChat from "./features/VideoChat/VideoChat";
import Email from "./features/Email/Email";

export default function Home() {
  const { token } = theme.useToken();
  const wrapperStyle: React.CSSProperties = {
    width: 300,
    border: `1px solid ${token.colorBorderSecondary}`,
    borderRadius: token.borderRadiusLG,
  };

  return (
    <React.Fragment>
      <Row gutter={16}>
        <Col span={8}>
          <Office />
        </Col>
        <Col span={8}>
          <Chat />
        </Col>
        <Col span={8}>
          <Docs />
        </Col>
      </Row>
      <Row gutter={16} style={{ marginTop: 10 }}>
        <Col span={8}>
          <Email />
        </Col>
        <Col span={8}>
          <VideoChat />
        </Col>
        <Col span={8}>
          <Card title="Agenda" variant="borderless">
            <div style={wrapperStyle}>
              <Calendar fullscreen={false} onPanelChange={undefined} />
            </div>
          </Card>
        </Col>
      </Row>
    </React.Fragment>
  );
}
