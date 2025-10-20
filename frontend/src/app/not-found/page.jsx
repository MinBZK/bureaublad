import React from "react";
import { Button, Result } from "antd";

function NotFound() {
  return (
    <React.Fragment>
      <Result
        status="404"
        title="404"
        subTitle="Er is iets mis gegaan"
        extra={
          <Button type="primary" href="/">
            Terug naar homepagina
          </Button>
        }
      />
    </React.Fragment>
  );
}

export default NotFound;
