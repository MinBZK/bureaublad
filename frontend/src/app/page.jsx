"use client";
import React from "react";
import { Col, Row, Card, Calendar, theme, Space } from "antd";
import Office from "./features/Office/Office";
import Chat from "./features/Chat/Chat";
import Docs from "./features/Docs/Docs";
import VideoChat from "./features/VideoChat/VideoChat";
import Email from "./features/Email/Email";
import { useAppContext } from "./Context/AppContext";
import DynamicIcon from "./Common/DynamicIcon";

export default function Home() {
  const { token } = theme.useToken();
  const wrapperStyle = {
    width: 300,
    border: `1px solid ${token.colorBorderSecondary}`,
    borderRadius: token.borderRadiusLG,
  };
  const { items } = useAppContext();
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
      <Row gutter={16}>
        {items?.sidebar_links?.map((value) => (
          <Col span={8} style={{ marginTop: 10 }}>
            <Card
              title={
                <Space>
                  <DynamicIcon name={value?.icon}/>
                  {value?.title}
                </Space>
              }
              variant="borderless"
            >
              {value?.url}
            </Card>
          </Col>
        ))}
      </Row>
    </React.Fragment>
  );
}
