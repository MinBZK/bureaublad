"use client";
import { Layout } from "antd";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../Context/AppContext";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import { usePathname } from "next/navigation";
const { Content, Footer } = Layout;

export default function PageLayout({ children }) {
  const { appConfig, error } = useAppContext();
  const { data } = useFetchWithRefresh("/api/v1/auth/profile");
  const pathname = usePathname();

  const isLayoutHidden = ["/login", "/404"].includes(pathname);

  return !isLayoutHidden ? (
    <Layout>
      <HeaderLayout
        isProfile={!!error}
        profile={data?.name}
        applications={appConfig?.applications}
      />
      <Content className="layout-content">
        <div className="content">{children}</div>
      </Content>
      <Footer>Mijn Bureau ©{new Date().getFullYear()}</Footer>
    </Layout>
  ) : (
    <>{children}</>
  );
}
