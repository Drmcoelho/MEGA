import type { AppProps } from "next/app";
import { NextIntlProvider } from "next-intl";
import "../styles/global.css"; // se quiser criar

export default function App({ Component, pageProps }: AppProps) {
  return (
    <NextIntlProvider
      messages={pageProps.messages}
      locale={pageProps.locale || "pt"}
    >
      <Component {...pageProps} />
    </NextIntlProvider>
  );
}
