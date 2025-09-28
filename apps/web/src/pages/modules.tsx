import { GetStaticProps } from 'next'
import Link from 'next/link'
import { loadModules, ModuleManifest } from '../utils/modules'

interface ModulesProps {
  modules: ModuleManifest[]
}

export default function Modules({ modules }: ModulesProps) {
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial, sans-serif' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1>Módulos Educacionais</h1>
        <p>Explore todos os módulos disponíveis na plataforma MEGA.</p>
        <p>
          <Link href="/" style={{ color: '#0070f3', textDecoration: 'none' }}>← Voltar ao início</Link>
        </p>
      </header>

      {modules.length > 0 ? (
        <div style={{ display: 'grid', gap: '2rem' }}>
          {modules.map((module) => (
            <div 
              key={module.id} 
              style={{ 
                border: '1px solid #ddd', 
                borderRadius: '12px', 
                padding: '1.5rem',
                backgroundColor: '#fdfdfd'
              }}
            >
              <div style={{ marginBottom: '1rem' }}>
                <h2>{module.title}</h2>
                <p style={{ color: '#666', margin: '0.5rem 0' }}>
                  Versão {module.version} • {module.estimated_time_hours} horas estimadas
                </p>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <h3>Objetivos de Aprendizagem</h3>
                <ul>
                  {module.objectives.map((obj, idx) => (
                    <li key={idx}>{obj}</li>
                  ))}
                </ul>
              </div>

              {module.subskills.length > 0 && (
                <div style={{ marginBottom: '1rem' }}>
                  <h4>Habilidades Desenvolvidas</h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                    {module.subskills.map((skill, idx) => (
                      <span 
                        key={idx}
                        style={{ 
                          backgroundColor: '#e3f2fd', 
                          padding: '0.25rem 0.75rem', 
                          borderRadius: '16px',
                          fontSize: '0.875rem'
                        }}
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {module.prerequisites.length > 0 && (
                <div style={{ marginBottom: '1rem' }}>
                  <h4>Pré-requisitos</h4>
                  <p>{module.prerequisites.join(', ')}</p>
                </div>
              )}

              {module.disclaimer && (
                <div style={{ 
                  backgroundColor: '#fff3cd', 
                  border: '1px solid #ffeeba',
                  padding: '1rem',
                  borderRadius: '6px',
                  marginTop: '1rem'
                }}>
                  <strong>Aviso:</strong> {module.disclaimer}
                </div>
              )}
            </div>
          ))}
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <h2>Nenhum módulo encontrado</h2>
          <p>Verifique se os arquivos manifest.yaml estão presentes em content/modules/</p>
        </div>
      )}
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