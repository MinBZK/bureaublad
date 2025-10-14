import { StarFilled, StarOutlined } from "@ant-design/icons";
import { Button, Card, Divider, Result, Input } from "antd";
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
    <Card
      title={title}
      variant="borderless"
      loading={loading}
      extra={
        setFavorite && (
          <Button
            onClick={() => setFavorite(!favorite)}
            type="text"
            icon={favorite ? <StarFilled /> : <StarOutlined />}
          />
        )
      }
      type="inner"
    >
      {error ? (
        <Result status="warning" title={error} style={{ marginTop: "-10%" }} />
      ) : (
        <React.Fragment>
          {setSearch && (
            <React.Fragment>
              <Search
                placeholder={`${title} zoeken`}
                onSearch={(t) => setSearch(t)}
                onChange={(e) => setValue(e.target.value)}
                value={value}
                allowClear
              />
              <Divider />
            </React.Fragment>
          )}

          {children}
        </React.Fragment>
      )}
    </Card>
  );
}

export default Widget;
