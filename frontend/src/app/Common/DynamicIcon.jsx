"use client";
import React from "react";

function DynamicIcon({ name }) {
  const [Icon, setIcon] = React.useState(null);

  React.useEffect(() => {
    import("@ant-design/icons")
      .then((icons) => {
        const ImportedIcon = icons[name];
        if (ImportedIcon) {
          setIcon(() => ImportedIcon);
        } else {
          setIcon(null);
        }
      })
      .catch(() => setIcon(null));
  }, [name]);

  return Icon ? <Icon /> : null;
}

export default DynamicIcon;
