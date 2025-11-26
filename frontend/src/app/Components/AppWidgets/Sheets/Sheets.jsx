// grist
import { useState, useEffect } from "react";
import { Avatar, Divider, List, Select } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "../../../Common/Widget";
import moment from "moment";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";

function Sheets({ title = "Sheets" }) {
  const selectedOrgStorage = localStorage.getItem("sheets_selected_org");
  const [selectedOrg, setSelectedOrg] = useState(selectedOrgStorage || null);
  const [page, setPage] = useState(1);
  const {
    data: orgs,
    loading: loadingOrgs,
    error: errorOrgs,
    onRefresh: refetchOrgs,
  } = useFetchWithRefresh("/api/v1/grist/orgs");

  const effectiveSelectedOrg =
    selectedOrg || (orgs.length > 0 ? orgs[0]?.id : null);

  const {
    data: sheets,
    loading: loadingSheets,
    error: errorSheets,
    onRefresh: refetchSheets,
  } = useFetchWithRefresh("/api/v1/grist/docs", {
    organization_id: effectiveSelectedOrg,
    page,
    page_size: 3,
  });

  useEffect(() => {
    if (!selectedOrg && orgs.length > 0) {
      localStorage.setItem("sheets_selected_org", orgs?.at(0)?.id);
    }
  }, [orgs, selectedOrg]);

  const handleOrgChange = (value) => {
    setSelectedOrg(value);
    localStorage.setItem("sheets_selected_org", value);
  };

  const orgOptions = orgs.slice(0, 2).map((org) => ({
    label: org.name,
    value: org.id,
  }));

  const onRefresh = () => {
    refetchSheets();
    refetchOrgs();
  };

  return (
    <Widget
      title={title}
      onRefresh={onRefresh}
      error={errorSheets || errorOrgs}
      page={page}
      setPage={setPage}
      total={sheets?.count}
    >
      <Select
        loading={loadingOrgs}
        showSearch
        placeholder="Organisatie selecteren"
        optionFilterProp="label"
        onChange={handleOrgChange}
        defaultValue={parseInt(effectiveSelectedOrg)}
        value={parseInt(effectiveSelectedOrg)}
        className="sheets-org-select"
        options={orgOptions}
      />
      <Divider />
      <List
        className="widget-list"
        loading={loadingSheets}
        dataSource={sheets?.results || []}
        renderItem={(item) => (
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
        )}
      />
    </Widget>
  );
}

export default Sheets;
