import { GetStaticProps } from 'next'
import Link from 'next/link'
import { loadModules, ModuleManifest } from '../utils/modules'

interface HomeProps {
  modules: ModuleManifest[]
}

export default function Home({ modules }: HomeProps) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1>MEGA - Medical Education with Generative AI</h1>
        <p>Plataforma inteligente para educação médica personalizada com IA generativa.</p>
      </header>

      <section style={{ marginBottom: '2rem' }}>
        <h2>Módulos Disponíveis ({modules.length})</h2>
        {modules.length > 0 ? (
          <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
            {modules.map((module) => (
              <div 
                key={module.id} 
                style={{ 
                  border: '1px solid #ddd', 
                  borderRadius: '8px', 
                  padding: '1rem',
                  backgroundColor: '#f9f9f9'
                }}
              >
                <h3>{module.title}</h3>
                <p><strong>Tempo estimado:</strong> {module.estimated_time_hours}h</p>
                <p><strong>Objetivos:</strong></p>
                <ul>
                  {module.objectives.slice(0, 3).map((obj, idx) => (
                    <li key={idx}>{obj}</li>
                  ))}
                </ul>
                {module.prerequisites.length > 0 && (
                  <p><strong>Pré-requisitos:</strong> {module.prerequisites.join(', ')}</p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p>Nenhum módulo encontrado. Verifique se os manifests estão em content/modules/</p>
        )}
      </section>

      <section>
        <h2>Funcionalidades</h2>
        <ul>
          <li>✨ Conteúdo adaptativo personalizado com IA</li>
          <li>📚 Múltiplos módulos educacionais especializados</li>
          <li>🤖 Orquestração multi-LLM (Gemini, GPT, etc.)</li>
          <li>🎯 Avaliação contínua e adaptativa</li>
          <li>⚡ Interface web moderna e responsiva</li>
        </ul>
        
        <p style={{ marginTop: '1rem' }}>
          <Link href="/modules" style={{ 
            color: '#0070f3', 
            textDecoration: 'none',
            border: '1px solid #0070f3',
            padding: '0.5rem 1rem',
            borderRadius: '4px'
          }}>
            Ver todos os módulos →
          </Link>
        </p>
      </section>
    </div>
  )
}

export const getStaticProps: GetStaticProps = async () => {
  const modules = loadModules()
  
  return {
    props: {
      modules,
    },
  }
}