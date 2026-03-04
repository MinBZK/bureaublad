"use client";
import {
  StarFilled,
  StarOutlined,
  ReloadOutlined,
  ArrowRightOutlined,
} from "@ant-design/icons";
import { Button, Card, Divider, Result, Input, Pagination } from "antd";
import React, { useState } from "react";
import Link from "next/link";
import { useTranslations } from "../../i18n/TranslationsProvider";

const { Search } = Input;

function Widget({
  children,
  title,
  app,
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
}) {
  const t = useTranslations("Widget");
  const [value, setValue] = useState("");

  return (
    <Card
      title={
        app ? (
          <Link
            href={app.iframe ? `/${app.id}` : app.url}
            target={app.iframe ? undefined : "_blank"}
            rel={app.iframe ? undefined : "noopener noreferrer"}
            className="widget-title-link"
          >
            {title} <ArrowRightOutlined className="widget-title-icon" />
          </Link>
        ) : (
          title
        )
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
        <div className="widget-body">
          {(setSearch || setFavorite) && (
            <div className="widget-search-row">
              {setSearch && (
                <Search
                  placeholder=""
                  onSearch={(t) => setSearch(t)}
                  onChange={(e) => setValue(e.target.value)}
                  value={value}
                  allowClear
                  className="widget-search"
                  style={{ flex: 1 }}
                />
              )}
              {setFavorite && (
                <Button
                  onClick={() => setFavorite(!favorite)}
                  type="text"
                  icon={favorite ? <StarFilled /> : <StarOutlined />}
                />
              )}
            </div>
          )}

          {children}

          {page && setPage && total > 3 && (
            <div className="widget-pagination">
              <Divider style={{ marginTop: 0 }} />
              <Pagination
                pageSize={3}
                defaultCurrent={page}
                current={page}
                onChange={(page) => setPage(page)}
                total={total}
                align="end"
                pageSizeOptions={[5]}
              />
            </div>
          )}
        </div>
      )}
    </Card>
  );
}

export default Widget;
