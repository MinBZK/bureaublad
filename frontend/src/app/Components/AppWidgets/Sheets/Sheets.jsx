// grist
import { useState, useEffect } from "react";
import { Avatar, Divider, List, Select } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import axios from "axios";
import Widget from "../../../Common/Widget";
import moment from "moment";

function Sheets() {
  const selectedOrgStorage = localStorage.getItem("sheets_selected_org");
  const [sheets, setSheets] = useState([]);
  const [orgs, setOrgs] = useState([]);
  const [loadingOrgs, setLoadingOrgs] = useState(false);
  const [errorOrgs, setErrorOrgs] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedOrg, setSelectedOrg] = useState(selectedOrgStorage || null);

  useEffect(() => {
    setLoadingOrgs(true);
    const fetchOrgs = async () => {
      try {
        const res = await axios.get(`/api/v1/grist/orgs`);
        setOrgs(res.data);
        if (!selectedOrg && res.data.length > 0) {
          setSelectedOrg(res.data[0]?.id);
          localStorage.setItem("sheets_selected_org", res.data[0]?.id);
        }
      } catch (err) {
        setErrorOrgs(err.message);
      } finally {
        setLoadingOrgs(false);
      }
    };
    fetchOrgs();
  }, [selectedOrg]);

  useEffect(() => {
    if (!selectedOrg) return;

    setLoading(true);
    const fetchSheets = async () => {
      try {
        const res = await axios.get(
          `/api/v1/grist/docs?organization_id=${selectedOrg}&page=1&page_size=3`,
        );
        setSheets(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchSheets();
  }, [selectedOrg]);

  const handleOrgChange = (value) => {
    setSelectedOrg(value);
    localStorage.setItem("sheets_selected_org", value);
  };

  const orgOptions = orgs.slice(0, 2).map((org) => ({
    label: org.name,
    value: org.id,
  }));

  return (
    <Widget title="Sheets" loading={loadingOrgs} error={error || errorOrgs}>
      <Select
        showSearch
        placeholder="Organisatie selecteren"
        optionFilterProp="label"
        onChange={handleOrgChange}
        defaultValue={parseInt(selectedOrg)}
        value={parseInt(selectedOrg)}
        className="sheets-org-select"
        options={orgOptions}
      />
      <Divider />
      <List
        loading={loading}
        dataSource={sheets}
        renderItem={(item, index) =>
          index <= 2 && (
            <List.Item key={item.description}>
              <List.Item.Meta
                avatar={<Avatar icon={<FileTextOutlined />} />}
                title={<Link href={item?.url}>{item.name}</Link>}
                description={`Geüpdatet: ${moment(item.updatedAt).format("DD-MM-YYYY")}`}
              />
              <Link href={item?.url}>
                <EditOutlined />
              </Link>
            </List.Item>
          )
        }
      />
    </Widget>
  );
}

export default Sheets;
