import { StarFilled, StarOutlined, ReloadOutlined } from "@ant-design/icons";
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

const { Search } = Input;

function Widget({
  children,
  title,
  error,
  loading = false,
  favorite,
  setFavorite = undefined,
  setSearch = undefined,
  placeholder = "",
  onRefresh = undefined,
  page = 1,
  setPage = undefined,
  total=10,
}) {
  const [value, setValue] = useState("");
  return (
    <Card
      title={title}
      variant="borderless"
      loading={loading}
      type="inner"
      extra={
        onRefresh && (
          <Button
            onClick={onRefresh}
            type="text"
            icon={<ReloadOutlined />}
            title="Vernieuwen"
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
                    placeholder={placeholder || `${title} zoeken`}
                    onSearch={(t) => setSearch(t)}
                    onChange={(e) => setValue(e.target.value)}
                    value={value}
                    allowClear
                    style={{ width: "100%" }}
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
          <Divider />
          <Pagination
            defaultCurrent={page}
            current={page}
            onChange={(page) => setPage(page)}
            total={total}
            align="end"
            pageSizeOptions={[5]}
          />
        </React.Fragment>
      )}
    </Card>
  );
}

export default Widget;
