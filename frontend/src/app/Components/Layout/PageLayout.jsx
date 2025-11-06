"use client";
import { Layout } from "antd";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../Context/AppContext";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
const { Content } = Layout;

export default function PageLayout({ children }) {
  const { items, error } = useAppContext();
  const { data } = useFetchWithRefresh("/api/v1/auth/profile");

  return (
    <Layout>
      <HeaderLayout
        isProfile={!!error}
        profile={data?.name}
        applications={items?.applications}
      />
      <Layout className="layout-content">
        <Content className="content">{children}</Content>
      </Layout>
    </Layout>
  );
}
