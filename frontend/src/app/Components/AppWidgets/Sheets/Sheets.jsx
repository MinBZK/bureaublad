// grist
import { useState, useEffect } from "react";
import { Divider, Select } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import Widget from "../../../Common/Widget";
import moment from "moment";
import { useFetchWithRefresh } from "@/app/Common/CustomHooks/useFetchWithRefresh";
import { useTranslations } from "../../../../i18n/TranslationsProvider";
import CustomList from "../../../Common/CustomList";

function Sheets({ app }) {
  const selectedOrgStorage = localStorage.getItem("sheets_selected_org");
  const [selectedOrg, setSelectedOrg] = useState(selectedOrgStorage || null);
  const [page, setPage] = useState(1);
  const t = useTranslations("Sheets");
  const {
    data: orgs,
    loading: loadingOrgs,
    error: errorOrgs,
    onRefresh: refetchOrgs,
  } = useFetchWithRefresh("/grist/orgs");

  const effectiveSelectedOrg =
    selectedOrg || (orgs.length > 0 ? orgs[0]?.id : null);

  const {
    data: sheets,
    loading: loadingSheets,
    error: errorSheets,
    onRefresh: refetchSheets,
  } = useFetchWithRefresh("/grist/docs", {
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
      title={t("title")}
      app={app}
      onRefresh={onRefresh}
      error={errorSheets || errorOrgs}
      page={page}
      setPage={setPage}
      total={sheets?.count}
    >
      <Select
        loading={loadingOrgs}
        showSearch
        placeholder={t("selectOrganization")}
        onChange={handleOrgChange}
        defaultValue={parseInt(effectiveSelectedOrg)}
        value={parseInt(effectiveSelectedOrg)}
        className="sheets-org-select"
        options={orgOptions}
      />
      <Divider />
      <CustomList
        className="widget-list"
        loading={loadingSheets}
        dataSource={sheets?.results || []}
        renderItem={(item) => (
          <CustomList.Item key={item.description}>
            <CustomList.Item.Meta
              avatar={<FileTextOutlined className="widget-icon-orange" />}
              title={
                <Link
                  href={item?.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {item.name}
                </Link>
              }
              description={`${t("update")}: ${moment(item.updatedAt).format("DD-MM-YYYY")}`}
            />
            <Link href={item?.url} target="_blank" rel="noopener noreferrer">
              <EditOutlined />
            </Link>
          </CustomList.Item>
        )}
      />
    </Widget>
  );
}

export default Sheets;
