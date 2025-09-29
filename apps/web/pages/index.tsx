import Link from "next/link";
import { GetStaticProps } from "next";
import { useTranslations } from "next-intl";
import { loadMessages } from "../lib/loadMessages";

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  return {
    props: {
      messages: await loadMessages(locale || "pt"),
      locale: locale || "pt",
    },
  };
};

export default function Home() {
  const t = useTranslations();
  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>{t("home.title")}</h1>
      <p>{t("home.intro")}</p>
      <ul>
        <li>
          <Link href="/modules">{t("nav.modules")}</Link>
        </li>
        <li>
          <Link href="/adaptive">{t("nav.adaptive")}</Link>
        </li>
      </ul>
    </main>
  );
}
