import { Flex, Spin } from "antd";
import React from "react";

function Loading({ loading, children }) {
  return loading ? (
    <div style={{ marginTop: 200 }}>
      <Spin size="large" style={{ display: "block", margin: "auto" }} />
    </div>
  ) : (
    children
  );
}

export default Loading;
