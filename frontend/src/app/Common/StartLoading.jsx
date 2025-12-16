
import Loading from "./Loading";

function StartLoading({ loading, children }) {
  return loading ? <Loading /> : children;
}

export default StartLoading;
