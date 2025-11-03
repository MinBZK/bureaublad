// grist
import { useState, useEffect } from "react";
import { Avatar, Divider, List, Radio } from "antd";
import { EditOutlined, FileTextOutlined } from "@ant-design/icons";
import Link from "next/link";
import axios from "axios";
import Widget from "../../../Common/Widget";
import moment from "moment";

function Sheets() {
  const [sheets, setSheets] = useState([]);
  const [orgs, setOrgs] = useState([]);
  const [loadingOrgs, setLoadingOrgs] = useState(false);
  const [errorOrgs, setErrorOrgs] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    setLoading(true);
    const fetchSheets = async () => {
      try {
        const res = await axios.get(`/api/v1/grist/docs?page=1&page_size=3`);
        setSheets(res.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchSheets();
  }, []);

  useEffect(() => {
    setLoadingOrgs(true);
    const fetchOrgs = async () => {
      try {
        const res = await axios.get(`/api/v1/grist/orgs?page=1&page_size=3`);
        setOrgs(res.data);
      } catch (err) {
        setErrorOrgs(err.message);
      } finally {
        setLoadingOrgs(false);
      }
    };
    fetchOrgs();
  }, []);

  return (
    <Widget
      title="Sheets"
      loading={loading || loadingOrgs}
      error={error || errorOrgs}
    >
      <Radio.Group
        block
        options={orgs.map((org) => ({
          label: org.name,
          value: org.id,
        }))}
        defaultValue="Pear"
        optionType="button"
      />
      <Divider />
      <List
        dataSource={sheets.filter((item) =>
          item.name.toLowerCase().includes(search.toLowerCase()),
        )}
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
