"use client";
import {
  StarFilled,
  StarOutlined,
  ReloadOutlined,
  ArrowRightOutlined,
  SettingOutlined,
} from "@ant-design/icons";
import {
  Button,
  Card,
  Divider,
  Result,
  Input,
  Row,
  Col,
  Pagination,
  Dropdown,
  Space,
} from "antd";
import React, { useState } from "react";
import { useTranslations } from "../../i18n/TranslationsProvider";
import Link from "next/link";
const { Search } = Input;

function Widget({
  children,
  error,
  loading = false,
  favorite,
  setFavorite = undefined,
  setSearch = undefined,
  placeholder = "",
  onRefresh = undefined,
  page = 1,
  setPage = undefined,
  total = 0,
  app,
  isAdmin = false,
}) {
  const t = useTranslations("Widget");
  const [value, setValue] = useState("");
  const { iframe, url, title, id } = app || {};
  const iconLink = (title) =>
    iframe && id ? (
      <Link href={`/${id}`}>{title}</Link>
    ) : (
      <Link href={url || ""} rel="noopener noreferrer" target="_blank">
        {title}
      </Link>
    );

  const items = [
    isAdmin && {
      label: (
        <Link
          href={id === "ocs" ? `${url}/settings/admin` : `${url}/admin` || ""}
          rel="noopener noreferrer"
          target="_blank"
        >
          <ArrowRightOutlined /> {title} {t("admin")}
        </Link>
      ),
      key: "0",
    },
    onRefresh && {
      label: (
        <Link onClick={onRefresh} href="#">
          <ReloadOutlined /> {t("refresh")}
        </Link>
      ),
      key: "1",
    },
  ];

  return (
    <Card
      title={<span>{iconLink(title)}</span>}
      loading={loading}
      extra={
        items.filter(Boolean).length > 0 && (
          <Dropdown menu={{ items: items.filter(Boolean) }} trigger={["click"]}>
            <a onClick={(e) => e.preventDefault()}>
              <Space>
                <SettingOutlined />
              </Space>
            </a>
          </Dropdown>
        )
      }
    >
      {error ? (
        <Result status="warning" title={error} className="space-min-up" />
      ) : (
        <React.Fragment>
          <Row>
            <Col span={setFavorite ? 22 : 24}>
              {setSearch && (
                <React.Fragment>
                  <Search
                    placeholder={placeholder || `${title} ${t("search")}`}
                    onSearch={(t) => setSearch(t)}
                    onChange={(e) => setValue(e.target.value)}
                    value={value}
                    allowClear
                    className="widget-search"
                  />
                  <Divider />
                </React.Fragment>
              )}
            </Col>
            <Col span={1} push={1}>
              {setFavorite && (
                <Button
                  onClick={() => setFavorite(!favorite)}
                  type="text"
                  icon={favorite ? <StarFilled /> : <StarOutlined />}
                />
              )}
            </Col>
          </Row>

          {children}

          {page && setPage && (
            <React.Fragment>
              <Divider />
              <Pagination
                pageSize={3}
                defaultCurrent={page}
                current={page}
                onChange={(page) => setPage(page)}
                total={total}
                align="end"
                pageSizeOptions={[5]}
              />
            </React.Fragment>
          )}
        </React.Fragment>
      )}
    </Card>
  );
}

export default Widget;
