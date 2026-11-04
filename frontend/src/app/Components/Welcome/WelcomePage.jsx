"use client";

import {
  CalendarOutlined,
  CloudOutlined,
  FileTextOutlined,
  FolderOpenOutlined,
  MessageOutlined,
  ProjectOutlined,
  TableOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";
import { useTranslations } from "../../../i18n/TranslationsProvider";

const WELCOME_ICONS = [
  FolderOpenOutlined,
  FileTextOutlined,
  TableOutlined,
  VideoCameraOutlined,
  MessageOutlined,
  CalendarOutlined,
  ProjectOutlined,
  CloudOutlined,
];

function WelcomePage({ onLogin, loginError = false }) {
  const t = useTranslations("Welcome");

  return (
    <section className="rh-welcome">
      <div className="rh-welcome-card">
        <div className="rh-welcome-content">
          <h1 className="rh-welcome-title">{t("title")}</h1>
          <p className="rh-welcome-text">{t("intro")}</p>

          {loginError && (
            <div className="rh-welcome-alert" role="alert">
              {t("loginError")}{" "}
              <a href="mailto:mijnbureau@rijksoverheid.nl">{t("helpdesk")}</a>
            </div>
          )}

          <button type="button" className="rh-login-button" onClick={onLogin}>
            {t("login")}
          </button>
          <p className="rh-welcome-hint">{t("loginHint")}</p>
        </div>

        <div className="rh-welcome-visual" aria-hidden="true">
          <div className="rh-welcome-grid">
            {WELCOME_ICONS.map((Icon, index) => (
              <span key={index} className="rh-welcome-icon">
                <Icon />
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

export default WelcomePage;
