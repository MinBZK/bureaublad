export default function LifecycleTag({
  status,
  mode,
}: {
  status: "Productie" | "In ontwikkeling" | "Proef";
  mode: "short" | "long";
}) {
  if (status === "Productie") {
    return;
  }

  const tagType = status === "In ontwikkeling" ? "warning" : "info";
  const tagIcon =
    status === "In ontwikkeling"
      ? "rvo-icon-kist-met-hamer-en-moersleutel"
      : "rvo-icon-tandwielen";
  const tagIconLabel =
    status === "In ontwikkeling"
      ? "Kist met hamer en moersleutel"
      : "Tandwielen";

  if (mode === "short") {
    return (
      <div
        title={status}
        className={"rvo-tag rvo-tag--with-icon rvo-tag--" + tagType}
      >
        <span
          className={
            "utrecht-icon rvo-icon " +
            tagIcon +
            " rvo-icon--md rvo-link__icon--before rvo-margin-inline-start--xs"
          }
          role="img"
          aria-label={tagIconLabel}
        ></span>
      </div>
    );
  } else {
    return (
      <div
        className={
          "rvo-tag rvo-tag--with-icon rvo-tag--" +
          tagType +
          " rvo-text--sm rvo-margin-inline-start--sm openbsw-lifecycle-long"
        }
      >
        <span
          className={
            "utrecht-icon rvo-icon " +
            tagIcon +
            " rvo-icon--md rvo-link__icon--before"
          }
          role="img"
          aria-label={tagIconLabel}
        ></span>
        {status}
      </div>
    );
  }
}
