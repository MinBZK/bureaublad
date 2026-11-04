"use client";

import { CheckOutlined } from "@ant-design/icons";
import { useTranslations } from "../../../../i18n/TranslationsProvider";

function ColorPicker({ brand, onSelect, palettes }) {
  const t = useTranslations("Theme");

  return (
    <div className="rh-colorpicker">
      <p className="rh-colorpicker-title">{t("paletteTitle")}</p>

      <div className="rh-colorpicker-grid">
        {Object.entries(palettes).map(([key, palette]) => {
          const isSelected = brand === key;

          return (
            <button
              key={key}
              type="button"
              className={
                isSelected
                  ? "rh-colorpicker-option is-selected"
                  : "rh-colorpicker-option"
              }
              onClick={() => onSelect(key)}
              aria-pressed={isSelected}
            >
              <span
                className="rh-colorpicker-swatch"
                style={{
                  backgroundColor: palette.hex,
                  color: palette.onPrimary,
                }}
                aria-hidden="true"
              >
                {isSelected && <CheckOutlined />}
              </span>
              <span className="rh-colorpicker-label">
                {palette.label}
              </span>
            </button>
          );
        })}
      </div>

      <p className="rh-colorpicker-note">{t("paletteHint")}</p>
    </div>
  );
}

export default ColorPicker;
