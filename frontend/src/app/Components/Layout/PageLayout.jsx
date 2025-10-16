"use client";
<<<<<<< HEAD
import { useState, useEffect } from "react";
import { Divider, Typography, Layout, theme, Skeleton } from "antd";
import SiderLayout from "./Components/SiderLayout";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../Context/AppContext";
import axios from "axios";
=======
import React, { useState, useEffect } from "react";
import { Divider, Typography, Layout, theme, Skeleton } from "antd";
import SiderLayout from "./Components/SiderLayout";
import HeaderLayout from "./Components/HeaderLayout";
import { useAppContext } from "../../Context/AppContext";
import axios from "axios";
import { baseUrl } from "../../Common/pageConfig";
>>>>>>> 800ac10 (✨(frontend) add conv and meeting)
const { Content } = Layout;

export default function PageLayout({ children }) {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
<<<<<<< HEAD
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
=======
  // const keycloakContext = useContext(KeycloakContext);
  const { items, error } = useAppContext();
>>>>>>> 800ac10 (✨(frontend) add conv and meeting)

  useEffect(() => {
    setLoading(true);
    const fetchProfile = async () => {
      try {
        const res = await axios.get(baseUrl + "/api/v1/ocs/activities");
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
      <HeaderLayout isProfile={!!error} />
      {error ? (
        children
      ) : (
        <Layout>
          <SiderLayout colorBgContainer={colorBgContainer} items={items} />
          <Layout style={{ padding: "0 24px 24px" }}>
            <Content
              style={{
                padding: 24,
                margin: 0,
                background: "#f5f5f5",
                borderRadius: borderRadiusLG,
              }}
            >
              <Skeleton loading={loading}>
<<<<<<< HEAD
                <Typography.Title>
                  Welkom
                  <span style={{ color: "#4096FF" }}>{profile?.name}</span>
                </Typography.Title>
=======
                <Typography.Title>Welkom {profile?.name}</Typography.Title>
>>>>>>> 800ac10 (✨(frontend) add conv and meeting)
              </Skeleton>
              <Divider />
              {children}
            </Content>
          </Layout>
        </Layout>
      )}
    </Layout>
  );
}
