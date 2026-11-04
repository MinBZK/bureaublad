"use client";
import { useEffect, useState } from "react";
import { Button, FloatButton, Layout, Result } from "antd";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../Context/AppContext";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import { useTranslations } from "../../../i18n/TranslationsProvider";
import WelcomePage from "../Welcome/WelcomePage";
import { MessageOutlined } from "@ant-design/icons";
const { Content, Footer } = Layout;

function AuthenticatedLayout({ appConfig, children }) {
  const t = useTranslations("Footer");
  const { data } = useFetchWithRefresh("/auth/profile");

  return (
    <Layout className="rh-layout">
      <HeaderLayout
        isAuthenticated
        profile={data?.name}
        redirectUrl={appConfig?.redirect_to_account_page}
        isAdmin={appConfig?.is_admin}
      />
      <Content className="layout-content">
        <div className="content">{children}</div>
      </Content>
      {appConfig?.helpdesk_url && (
        <FloatButton
          shape="circle"
          style={{ insetInlineEnd: 40, insetBlockEnd: 80 }}
          icon={<MessageOutlined />}
          href={appConfig?.helpdesk_url}
          tooltip={t("helpdesk")}
        />
      )}
      <Footer className="rh-footer">
        {t("copyright")} {new Date().getFullYear()}
      </Footer>
    </Layout>
  );
}

export default function PageLayout({ children }) {
  const { appConfig, error, retryConfig } = useAppContext();
  const tError = useTranslations("ErrorPage");
  const [loginError, setLoginError] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setLoginError(params.get("error") === "authentication_failed");
  }, []);

  const isUnauthenticated = error?.status === 401;
  const hasError = Boolean(error) && !isUnauthenticated;
  const isAuthenticated = Boolean(appConfig) && !error;

  const handleLogin = () => {
    const url = new URL(window.location.href);
    url.searchParams.delete("error");
    const redirectTo = url.pathname + url.search;
    window.location.href = `/api/v1/auth/login?redirect_to=${encodeURIComponent(
      redirectTo,
    )}`;
  };

  if (hasError) {
    return (
      <Layout className="rh-layout">
        <HeaderLayout isAuthenticated={false} />
        <Content className="rh-error-screen">
          <div className="rh-error-card">
            <Result
              status="500"
              title={tError("title")}
              subTitle={tError("subTitle")}
              extra={
                <Button type="primary" onClick={retryConfig}>
                  {tError("retry")}
                </Button>
              }
            />
          </div>
        </Content>
      </Layout>
    );
  }

  if (!isAuthenticated) {
    return (
      <Layout className="rh-layout">
        <HeaderLayout isAuthenticated={false} />
        <Content className="rh-welcome-content-area">
          <WelcomePage onLogin={handleLogin} loginError={loginError} />
        </Content>
      </Layout>
    );
  }

  return (
    <AuthenticatedLayout appConfig={appConfig}>{children}</AuthenticatedLayout>
  );
}
