import { Spin } from "antd";

function Loading() {
  return (
    <div className="loading-space-up">
      <Spin size="large" className="position-middle" />
    </div>
  );
}

export default Loading;
