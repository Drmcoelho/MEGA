import type { AppProps } from 'next/app';
import { NextIntlClientProvider } from 'next-intl';
// import '../styles/global.css'; // se quiser criar

export default function App({ Component, pageProps }: AppProps) {
  return (
    <NextIntlClientProvider messages={pageProps.messages} locale={pageProps.locale || 'pt'}>
      <Component {...pageProps} />
    </NextIntlClientProvider>
  );
}