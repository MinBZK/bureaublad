"use client";

import { useState } from "react";
import { useAppContext } from "../Components/Context/AppContext";
import { usePathname } from "next/navigation";
import { Dropdown, Affix } from "antd";
import {
  FullscreenOutlined,
  FullscreenExitOutlined,
  ExportOutlined,
  DownOutlined,
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

  const menuItems = [
    {
      key: "newTab",
      label: t("openNewTab"),
      icon: <ExportOutlined />,
      onClick: openInNewTab,
    },
    {
      key: "fullscreen",
      label: isFullscreen ? t("exitFullscreen") : t("fullscreen"),
      icon: isFullscreen ? <FullscreenExitOutlined /> : <FullscreenOutlined />,
      onClick: toggleFullscreen,
    },
  ];

  return (
    <div
      className={
        isFullscreen
          ? "external-app-container-fullscreen"
          : "external-app-container"
      }
    >
      <Dropdown
        menu={{ items: menuItems }}
        trigger={["hover"]}
        placement="bottomRight"
        getPopupContainer={(trigger) => trigger.parentElement}
        rootClassName="external-app-dropdown-menu"
      >
        <div className="external-app-dropdown-trigger">
          <DownOutlined
            style={{ fontSize: "10px", color: "rgba(255, 255, 255, 0.8)" }}
          />
        </div>
      </Dropdown>
      <iframe
        src={app?.url}
        className="external-app-iframe"
        title={app?.title}
        allow="camera *; microphone *; fullscreen *; display-capture *; autoplay *"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-popups-to-escape-sandbox allow-downloads allow-modals allow-storage-access-by-user-activation"
      />
    </div>
  );
}
