"use client";

import { KeycloakContext } from "../Context/auth/KeycloakProvider";
import { useContext } from "react";

export default function UserMenu() {
  const keycloakContext = useContext(KeycloakContext);

  return (
    <a className="rvo-link rvo-menubar__link rvo-link--logoblauw" href="#">
      <span
        className="utrecht-icon rvo-icon rvo-icon-user rvo-icon--md rvo-icon--hemelblauw"
        role="img"
        aria-label="Home"
      ></span>
      {keycloakContext.user.name}
    </a>
  );
}
