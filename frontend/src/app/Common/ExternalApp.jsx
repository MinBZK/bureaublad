"use client";

import { useState } from "react";
import { useAppContext } from "../Components/Context/AppContext";
import { usePathname } from "next/navigation";
import { Button, Tooltip } from "antd";
import {
  FullscreenOutlined,
  FullscreenExitOutlined,
  ExportOutlined,
} from "@ant-design/icons";
import { useTranslations } from "../../i18n/TranslationsProvider";

export default function ExternalApp() {
  const pathname = usePathname();
  const { appConfig } = useAppContext();
  const [isFullscreen, setIsFullscreen] = useState(false);
  const t = useTranslations("ExternalApp");
  const app = appConfig?.applications?.find(
    (application) => application.id === pathname.slice(1),
  );

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const openInNewTab = () => {
    window.open(app?.url, "_blank", "noopener,noreferrer");
  };

  return (
    <div
      style={{
        width: "100%",
        height: isFullscreen ? "100vh" : "calc(100vh - 64px)",
        position: isFullscreen ? "fixed" : "relative",
        top: isFullscreen ? 0 : "auto",
        left: isFullscreen ? 0 : "auto",
        zIndex: isFullscreen ? 9999 : "auto",
        backgroundColor: "#fff",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 10,
          right: 10,
          zIndex: 10000,
          display: "flex",
          gap: "8px",
        }}
      >
        <Tooltip title={t("openInNewTab")}>
          <Button
            icon={<ExportOutlined />}
            onClick={openInNewTab}
            type="default"
          />
        </Tooltip>
        <Tooltip title={isFullscreen ? t("exitFullscreen") : t("fullscreen")}>
          <Button
            icon={
              isFullscreen ? <FullscreenExitOutlined /> : <FullscreenOutlined />
            }
            onClick={toggleFullscreen}
            type="default"
          />
        </Tooltip>
      </div>
      <iframe
        src={app?.url}
        style={{
          width: "100%",
          height: "100%",
          border: "none",
        }}
        title={app?.title}
        allow="camera; microphone; fullscreen; display-capture"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-popups-to-escape-sandbox"
      />
    </div>
  );
}
