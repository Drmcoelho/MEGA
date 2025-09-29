import { GetStaticProps } from "next";
import Link from "next/link";
import { loadMessages } from "../../lib/loadMessages";
import { useTranslations } from "next-intl";
import { sampleMastery, dueItemsSample } from "../../lib/adaptiveSample";
import { RadialMastery } from "../../components/RadialMastery";

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  return {
    props: {
      messages: await loadMessages(locale || "pt"),
      locale: locale || "pt",
    },
  };
};

export default function AdaptiveDashboard() {
  const t = useTranslations();
  const mastery = sampleMastery();
  const due = dueItemsSample();
  return (
    <main style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>{t("adaptive.title")}</h1>
      <div style={{ display: "flex", gap: "2rem", flexWrap: "wrap" }}>
        <RadialMastery data={mastery} />
        <div style={{ minWidth: "260px" }}>
          <h2>Due Items</h2>
          <ul>
            {due.map((i) => (
              <li key={i}>{i}</li>
            ))}
          </ul>
        </div>
      </div>
      <p style={{ marginTop: "2rem" }}>
        <Link href="/">{t("nav.back")}</Link>
      </p>
    </main>
  );
}
