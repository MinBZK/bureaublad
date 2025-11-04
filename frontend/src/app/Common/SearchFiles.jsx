import React from "react";
import { useState } from "react";
import { Input, AutoComplete } from "antd";
import axios from "axios";

const { Search } = Input;

function SearchFiles() {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [inputValue, setInputValue] = useState("");
  const [filteredOptions, setFilteredOptions] = useState([]);
  const [open, setOpen] = useState(false);

  const handleSearchClick = async (text) => {
    if (!text) {
      setFilteredOptions([]);
      setOpen(false);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`/api/v1/ocs/search?term=${text}`);
      if (res.data.length > 0) {
        setFilteredOptions(
          res.data.map((value) => ({
            label: (
              <div
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => (window.location.href = value.url)}
              >
                {value?.name}
              </div>
            ),
            value: value?.name,
          })),
        );
      } else {
        setFilteredOptions([
          {
            label: "Not Found",
            value: "",
            disabled: true,
          },
        ]);
      }

      setOpen(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const onChangeInput = (e) => {
    setInputValue(e?.target?.value);
    if (e?.target?.value === "") {
      setOpen(false);
    }
  };

  return (
    <React.Fragment>
      <AutoComplete
        options={filteredOptions}
        open={open}
        value={inputValue}
        onBlur={() => setOpen(false)}
        className="sider-search"
      >
        <Search
          allowClear
          value={inputValue}
          onChange={onChangeInput}
          onSearch={handleSearchClick}
          loading={loading}
          placeholder="Bestanden zoeken..."
          variant="underlined"
          size="large"
        />
      </AutoComplete>
      <span className="side-search-error">{error && `Error: ${error}`}</span>
    </React.Fragment>
  );
}

export default SearchFiles;
