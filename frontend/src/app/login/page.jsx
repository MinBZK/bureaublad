import React from "react";
import { Button, Result } from "antd";

function Login() {
  return (
    <React.Fragment>
      <Result
        status="warning"
        title="Inloggen"
        subTitle="Helaas, u bent niet bevoegd om deze pagina te bezoeken."
        extra={
          <Button type="primary" href={`/api/v1/auth/login`}>
            Inloggen
          </Button>
        }
      />
    </React.Fragment>
  );
}

export default Login;
