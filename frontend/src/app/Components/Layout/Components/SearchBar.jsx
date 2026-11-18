"use client";
import { useRef, useState } from "react";
import { AutoComplete, Input, Tag } from "antd";
import { SearchOutlined } from "@ant-design/icons";
import api from "@/lib/axios";
import { useTranslations } from "../../../../i18n/TranslationsProvider";

const DEBOUNCE_MS = 300;

function SearchBar({ serviceTitles = {} }) {
  const tSearch = useTranslations("Search");
  const [options, setOptions] = useState([]);
  const resultsRef = useRef(new Map());
  const timerRef = useRef(null);

  const handleSearch = (value) => {
    if (timerRef.current) clearTimeout(timerRef.current);

    const q = value.trim();
    if (!q) {
      setOptions([]);
      return;
    }

    timerRef.current = setTimeout(async () => {
      try {
        const res = await api.get("/search", { params: { q } });
        const results = res?.data?.results ?? [];
        resultsRef.current = new Map(
          results.map((result) => [`${result.service}:${result.id}`, result]),
        );
        setOptions(
          results.map((result) => ({
            value: `${result.service}:${result.id}`,
            disabled: !result.url,
            label: (
              <div className="rh-search-result">
                <span className="rh-search-result-title">{result.title}</span>
                <span className="rh-search-result-meta">
                  <Tag>{serviceTitles[result.service] ?? result.service}</Tag>
                  {result.path && (
                    <span className="rh-search-result-path">{result.path}</span>
                  )}
                </span>
              </div>
            ),
          })),
        );
      } catch {
        setOptions([]);
      }
    }, DEBOUNCE_MS);
  };

  const handleSelect = (value) => {
    const result = resultsRef.current.get(value);
    if (result?.url) {
      window.open(result.url, "_blank", "noopener,noreferrer");
    }
  };

  return (
    <AutoComplete
      className="rh-search-autocomplete"
      options={options}
      onSearch={handleSearch}
      onSelect={handleSelect}
    >
      <Input
        allowClear
        prefix={<SearchOutlined />}
        placeholder={tSearch("placeholder")}
        aria-label={tSearch("placeholder")}
      />
    </AutoComplete>
  );
}

export default SearchBar;
