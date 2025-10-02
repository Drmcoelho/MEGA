import { GetStaticProps } from 'next';
import { loadManifests } from '../../lib/loadModules';
import Link from 'next/link';
import { loadMessages } from '../../lib/loadMessages';
import { useTranslations } from 'next-intl';

export const getStaticProps: GetStaticProps = async ({ locale }) => {
  const modules = loadManifests();
  return {
    props: {
      modules,
      messages: await loadMessages(locale || 'pt'),
      locale: locale || 'pt'
    }
  };
};

export default function ModulesPage({ modules }: {modules:any[]}) {
  const t = useTranslations();
  return (
    <main style={{padding:'2rem', fontFamily:'sans-serif'}}>
      <h1>{t('modules.title')}</h1>
      {modules.length === 0 && <p>—</p>}
      <ul>
        {modules.map(m => (
          <li key={m.id}>
            <strong>{m.title}</strong> <code>{m.id}</code> v{m.version || '0.1.0'}
          </li>
        ))}
      </ul>
      <p><Link href="/">{t('nav.back')}</Link></p>
    </main>
  );
}