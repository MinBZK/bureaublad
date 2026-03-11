import api from "./axios";

export async function attemptSilentLogin(redirectTo) {
  try {
    const params = new URLSearchParams();
    params.append("silent", "true");
    if (redirectTo) {
      params.append("redirect_to", redirectTo);
    }

    const response = await api.get(`/api/v1/auth/login?${params}`);
    return response.status === 200;
  } catch (error) {
    console.error("Silent login failed:", error);
    return false;
  }
}
