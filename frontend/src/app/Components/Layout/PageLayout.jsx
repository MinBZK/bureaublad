"use client";
import { FloatButton, Layout } from "antd";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../Context/AppContext";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import { usePathname } from "next/navigation";
import { useTranslations } from "../../../i18n/TranslationsProvider";
import ExternalApp from "@/app/Common/ExternalApp";
import { MessageOutlined } from "@ant-design/icons";
const { Content, Footer } = Layout;

export default function PageLayout({ children }) {
  const t = useTranslations("Footer");
  const { appConfig, error } = useAppContext();
  const { data } = useFetchWithRefresh("/auth/profile");
  const pathname = usePathname();

  const isLayoutHidden = ["/login"].includes(pathname);

  // Get all embedded apps (apps with iframe: true)
  const embeddedApps =
    appConfig?.applications?.filter((app) => app.iframe && app.url) || [];
  const currentAppId = pathname.slice(1); // Remove leading slash
  const isEmbeddedAppRoute = embeddedApps.some(
    (app) => app.id === currentAppId,
  );

  return !isLayoutHidden ? (
    <Layout>
      <HeaderLayout
        isProfile={!!error}
        profile={data?.name}
        applications={appConfig?.applications}
        redirectUrl={appConfig?.redirect_to_account_page}
      />
      <Content className="layout-content">
        <div className="content">
          {/* Render all embedded apps at once, show/hide based on route */}
          {embeddedApps.map((app) => {
            const isActive = currentAppId === app.id;
            const isMatrix = app.id === "matrix";

            return (
              <div
                key={app.id}
                style={{
                  // Use visibility:hidden for Matrix to prevent cache clearing issues
                  ...(isMatrix
                    ? {
                        visibility: isActive ? "visible" : "hidden",
                        position: isActive ? "relative" : "absolute",
                        height: "100%",
                        width: "100%",
                      }
                    : {
                        display: isActive ? "block" : "none",
                        height: "100%",
                      }),
                }}
              >
                <ExternalApp appId={app.id} />
              </div>
            );
          })}
          {/* Render children for non-embedded routes */}
          {!isEmbeddedAppRoute && children}
        </div>
      </Content>
      {appConfig?.helpdesk_url && (
        <FloatButton
          shape="circle"
          style={{ insetInlineEnd: 30 }}
          icon={<MessageOutlined />}
          href={appConfig?.helpdesk_url}
          tooltip={t("helpdesk")}
        />
      )}
      <Footer>
        {t("copyright")}
        {new Date().getFullYear()}
      </Footer>
    </Layout>
  ) : (
    <>{children}</>
  );
}
