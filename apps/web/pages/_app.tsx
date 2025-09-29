import type { AppProps } from 'next/app';
import { IntlProvider } from 'next-intl';
import '../styles/global.css'; // se quiser criar

export default function App({ Component, pageProps }: AppProps) {
  return (
    <IntlProvider messages={pageProps.messages} locale={pageProps.locale || 'pt'}>
      <Component {...pageProps} />
    </IntlProvider>
  );
}