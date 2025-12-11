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
      <Row gutter={16} className="dashboard-list">
        {appComponents.map((item, index) => (
          <Col key={index} xs={24} sm={24} md={24} lg={12} xl={12} xxl={8}>
            {item}
          </Col>
        ))}
      </Row>
  );
}
