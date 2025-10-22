import { StarFilled, StarOutlined } from "@ant-design/icons";
import { Button, Card, Divider, Result, Input, Row, Col } from "antd";
import React, { useState } from "react";

const { Search } = Input;

function Widget({
  children,
  title,
  error,
  loading,
  favorite,
  setFavorite,
  setSearch,
}) {
  const [value, setValue] = useState("");
  return (
    <Card title={title} variant="borderless" loading={loading} type="inner">
      {error ? (
        <Result status="warning" title={error} className="space-min-up" />
      ) : (
        <React.Fragment>
          <Row>
            <Col span={22}>
              {setSearch && (
                <React.Fragment>
                  <Search
                    placeholder={`${title} zoeken`}
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
        </React.Fragment>
      )}
    </Card>
  );
}

export default Widget;
