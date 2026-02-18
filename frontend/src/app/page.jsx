"use client";
import { Row, Col } from "antd";
import { useAppContext } from "./Components/Context/AppContext";
import { availableWidgetComponents } from "./Common/pageConfig";

export default function Home() {
  const { appConfig } = useAppContext();

  const appComponents = availableWidgetComponents(
    appConfig?.applications || [],
  );

  return (
    <Row gutter={10} className="dashboard-list">
      {appComponents.map((item, index) => (
        <Col key={index} xs={24} sm={24} md={12} lg={8} xl={8} xxl={8}>
          {item}
        </Col>
      ))}
    </Row>
  );
}
