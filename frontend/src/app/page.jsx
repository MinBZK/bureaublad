"use client";
import { Row, Col, Empty } from "antd";
import { useAppContext } from "./Components/Context/AppContext";
import { availableWidgetComponents } from "./Common/pageConfig";
import { useTranslations } from "../i18n/TranslationsProvider";

export default function Home() {
  const { appConfig } = useAppContext();
  const t = useTranslations("Dashboard");

  const appComponents = availableWidgetComponents(
    appConfig?.applications || [],
  );

  if (appComponents.length === 0) {
    return <Empty description={t("noApps")} style={{ marginTop: 80 }} />;
  }

  return (
    <Row gutter={16} className="dashboard-list">
      {appComponents.map((item, index) => (
        <Col key={index} xs={24} sm={12} md={12} lg={12} xl={12} xxl={8}>
          {item}
        </Col>
      ))}
    </Row>
  );
}
