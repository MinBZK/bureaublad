"use client";
import { useState, useEffect } from "react";
import { Divider, Typography, Layout, Skeleton, Flex } from "antd";
import SiderLayout from "./Components/SiderLayout";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../Context/AppContext";
import axios from "axios";
import SearchFiles from "../../Common/SearchFiles";

const { Content } = Layout;

export default function PageLayout({ children }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  const { items, error } = useAppContext();

  useEffect(() => {
    setLoading(true);
    const fetchProfile = async () => {
      try {
        const res = await axios.get("/api/v1/auth/profile");
        setProfile(res.data);
      } catch (err) {
        console.error(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  useEffect(() => {
    setLoading(true);
    const fetchProfile = async () => {
      try {
        const res = await axios.get("/api/v1/auth/profile");
        setProfile(res.data);
      } catch (err) {
        console.error(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  return (
    <Layout>
      <HeaderLayout isProfile={!!error} profile={profile?.name} />
      <Layout hasSider>
        <SiderLayout items={items} />
        <Layout className="layout-content">
          <Content className="content">
            <Skeleton loading={loading}>
              <Flex justify="space-between" align="center">
                <Typography.Title>
                  Welkom <span className="profile">{profile?.name}</span>
                </Typography.Title>
                <SearchFiles />
              </Flex>
            </Skeleton>
            <Divider />
            {children}
          </Content>
        </Layout>
      </Layout>
    </Layout>
  );
}
