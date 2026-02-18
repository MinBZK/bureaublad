const STORAGE_KEY = "silent-login-retry";
const silentLoginPath = "/api/v1/auth/login?silent=true";

// Checks if the user is allowed to attempt a silent login based on the last retry time stored in localStorage
function isRetryAllowed() {
  const lastRetryDate = localStorage.getItem(STORAGE_KEY);
  if (!lastRetryDate) {
    return true;
  }
  const now = new Date();
  return now.getTime() > Number(lastRetryDate);
}

// Sets the next allowed retry time in localStorage based on the current time and the specified retry interval
function setNextRetryTime(retryInSeconds) {
  const now = new Date();
  const nextRetryTime = now.getTime() + retryInSeconds * 1000;
  localStorage.setItem(STORAGE_KEY, nextRetryTime.toString());
}

// Initiates the silent login process by redirecting the user to the silent login URL
function initiateSilentLogin(redirectTo) {
  const silentLoginUrl = redirectTo
    ? `${silentLoginPath}&redirect_to=${encodeURIComponent(redirectTo)}`
    : `${silentLoginPath}`;

  window.location.href = silentLoginUrl;
}

// Attempt silent login with retry mechanism
export function attemptSilentLogin(retryInSeconds = 300, redirectTo) {
  if (!isRetryAllowed()) {
    return;
  }

  setNextRetryTime(retryInSeconds);
  initiateSilentLogin(redirectTo);
}
