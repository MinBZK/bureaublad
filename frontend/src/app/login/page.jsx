import React from "react";
import HeaderLayout from "../Components/Layout/Components/HeaderLayout";
import { Button, Result } from "antd";
import { baseUrl } from "../Common/pageConfig";

function Login() {
  return (
    <React.Fragment>
      <Result
        status="warning"
        title="Inloggen"
        subTitle="Helaas, u bent niet bevoegd om deze pagina te bezoeken."
        extra={
          <Button type="primary" href={`${baseUrl}/api/v1/auth/login`}>
            Inloggen
          </Button>
        }
      />
    </React.Fragment>
  );
}

export default Login;
