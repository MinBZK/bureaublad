import { Button, Result } from "antd";
import React from "react";

function ErrorResult({ errorStatus, title, subTitle, btnTitle, btnLink }) {
  return (
    <Result
      status={errorStatus}
      title={title}
      subTitle={subTitle}
      extra={
        <Button type="primary" href={btnLink}>
          {btnTitle}
        </Button>
      }
    />
  );
}

export default ErrorResult;
