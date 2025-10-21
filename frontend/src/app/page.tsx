import React from "react";
import { Col, Row, Card, Calendar } from "antd";
import Office from "./features/Office/Office";
import Chat from "./features/Chat/Chat";
import Docs from "./features/Docs/Docs";
import VideoChat from "./features/VideoChat/VideoChat";

export default function Home() {
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
            <Calendar fullscreen={false} onPanelChange={undefined} />
          </Card>
        </Col>
      </Row>
    </React.Fragment>
  );
}
