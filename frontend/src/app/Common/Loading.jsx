import { Spin } from "antd";

function Loading({ loading, children }) {
  return loading ? (
    <div className="loading-space-up">
      <Spin size="large" className="position-middle" />
    </div>
  ) : (
    children
  );
}

export default Loading;
