"use client";

import { useAppContext } from "../Components/Context/AppContext";
import { usePathname } from "next/navigation";

export default function ExternalApp() {
  const pathname = usePathname();
  const { appConfig } = useAppContext();
  const app = appConfig?.applications?.find(
    (application) => application.id === pathname.slice(1),
  );

  return (
    <div style={{ width: "100%", height: "calc(100vh - 64px)" }}>
      <iframe
        src={app?.url}
        style={{
          width: "100%",
          height: "100%",
          border: "none",
        }}
        title={app?.title}
        allow="fullscreen"
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-popups-to-escape-sandbox allow-downloads allow-modals allow-storage-access-by-user-activation"
      />
    </div>
  );
}
