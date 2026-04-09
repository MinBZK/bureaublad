"use client";
import { Card, Typography, Flex } from "antd";
import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAppContext } from "../Components/Context/AppContext";
import { useTranslations } from "../../i18n/TranslationsProvider";
import Link from "next/link";
const { Paragraph } = Typography;

export default function Admin() {
  const { appConfig } = useAppContext();
  const t = useTranslations("AdminPortal");
  const router = useRouter();
  useEffect(() => {
    if (!appConfig.isAdmin) {
      router.replace("/");
    }
  }, [appConfig.isAdmin, router]);

  const configUrl = (item) =>
    item?.id === "ocs"
      ? `${item?.url}/settings/admin`
      : `${item?.url}/admin` || "";
  return (
    appConfig.isAdmin && (
      <Card className="admin-portal" title={t("title")}>
        {t("description")}
        <ul>
          {appConfig?.applications.map(
            (item, index) =>
              item?.id !== "ai" && (
                <React.Fragment key={index}>
                  <li>
                    <Flex gap={1}>
                      {item.title} :
                      <Paragraph copyable>
                        <Link
                          href={configUrl(item)}
                          rel="noopener noreferrer"
                          target="_blank"
                        >
                          {configUrl(item)}
                        </Link>
                      </Paragraph>
                    </Flex>
                  </li>
                </React.Fragment>
              ),
          )}
        </ul>
      </Card>
    )
  );
}
