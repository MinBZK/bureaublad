import "./globals.css";
import "./custom-style.css";

import { AppProvider } from "./Components/Context/AppContext";
import ThemeLoader from "./Components/ThemeLoader/ThemeLoader";

export const metadata = {
  title: "Mijn Bureaublad",
  description: "Open BSW bureaublad",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body suppressHydrationWarning>
        <AppProvider>
          <ThemeLoader />
          {children}
        </AppProvider>
      </body>
    </html>
  );
}
