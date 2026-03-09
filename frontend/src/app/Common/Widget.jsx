"use client";
import {
  StarFilled,
  StarOutlined,
  ReloadOutlined,
  ArrowRightOutlined,
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
}) {
  const t = useTranslations("Widget");
  const [value, setValue] = useState("");
  const { iframe, url, title } = app || {};
  const iconLink = iframe ? (
    <Link href={`/${id}`}>
      <ArrowRightOutlined />
    </Link>
  ) : (
    <Link href={url || ""} rel="noopener noreferrer" target="_blank">
      <ArrowRightOutlined />
    </Link>
  );

  return (
    <Card
      title={
        <span>
          {title} {iconLink}
        </span>
      }
      loading={loading}
      extra={
        onRefresh && (
          <Button
            onClick={onRefresh}
            type="text"
            icon={<ReloadOutlined />}
            title={t("refresh")}
          />
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
