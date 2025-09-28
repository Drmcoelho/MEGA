# MEGA - Arquitetura do Sistema

## Visão Geral

O MEGA (Medical Education with Generative AI) é uma plataforma educacional médica que utiliza inteligência artificial generativa para personalizar o aprendizado. O sistema é organizado como um monorepo com arquitetura modular.

## Arquitetura de Alto Nível

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Content       │
│   (Next.js)     │◄───┤   (Node.js)     │◄───┤   (Markdown)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Tools     │    │  LLM Orchestr.  │    │  Content Engine │
│   (Python)      │    │   (Python)      │    │   (Node.js)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Componentes Principais

### 1. Frontend Web (apps/web)
- **Tecnologia**: Next.js 14 com TypeScript
- **Responsabilidades**:
  - Interface de usuário responsiva
  - Navegação entre módulos educacionais
  - Renderização de conteúdo Markdown
  - Apresentação de quizzes interativos
- **Integração**: Consome APIs dos serviços backend

### 2. CLI (packages/cli)
- **Tecnologia**: Python com Typer
- **Funcionalidades**:
  - Ingestão de conteúdo educacional
  - Geração de casos clínicos
  - Administração do sistema
  - Ferramentas de desenvolvimento

### 3. LLM Orchestrator (packages/llm-orchestrator)
- **Tecnologia**: Python com asyncio
- **Responsabilidades**:
  - Integração com múltiplos provedores de LLM
  - Roteamento inteligente de requisições
  - Fallback automático entre provedores
  - Otimização de custos e latência

### 4. Content Engine (packages/content-engine)
- **Tecnologia**: Node.js/TypeScript
- **Funcionalidades**:
  - Processamento de arquivos Markdown
  - Validação de manifests YAML
  - Indexação de conteúdo educacional
  - Extração de metadados

## Estrutura de Dados

### Módulos Educacionais
```yaml
id: string              # Identificador único
title: string           # Nome do módulo
version: string         # Versão semântica
objectives: string[]    # Objetivos de aprendizagem
subskills: string[]     # Habilidades desenvolvidas
prerequisites: string[] # Pré-requisitos
estimated_time_hours: number
disclaimer: string      # Avisos importantes
```

### Conteúdo de Lições
- **Formato**: Markdown com frontmatter YAML
- **Estrutura**: Hierárquica com seções e subseções
- **Elementos**: Texto, imagens, links, exercícios

### Quizzes
```json
{
  "id": "string",
  "title": "string",
  "questions": [
    {
      "type": "multiple_choice",
      "question": "string",
      "options": ["string"],
      "correct_answer": number,
      "explanation": "string"
    }
  ]
}
```

## Fluxo de Dados

### 1. Carregamento de Conteúdo
```
content/modules → Content Engine → Next.js Static Props → UI
```

### 2. Geração de Conteúdo
```
User Input → LLM Orchestrator → Provider APIs → Generated Content
```

### 3. Avaliação e Feedback
```
User Responses → Assessment Engine → Learning Analytics → Adaptive Content
```

## Padrões de Design

### 1. Modularidade
- Cada módulo educacional é independente
- Componentes reutilizáveis entre módulos
- Separação clara de responsabilidades

### 2. Extensibilidade
- Plugin system para novos tipos de conteúdo
- API para integração com sistemas externos
- Suporte a múltiplos formatos de avaliação

### 3. Escalabilidade
- Arquitetura stateless
- Caching estratégico
- Load balancing para LLMs

## Segurança e Privacidade

### Autenticação e Autorização
- JWT tokens para sessões
- Role-based access control (RBAC)
- OAuth2 para integração externa

### Proteção de Dados
- Criptografia de dados sensíveis
- Logs de auditoria
- Conformidade com LGPD/GDPR

### Rate Limiting
- Proteção contra abuse das APIs LLM
- Throttling baseado em usuário
- Monitoramento de uso

## Deployment e Infraestrutura

### Ambientes
- **Development**: Local com hot reload
- **Staging**: Ambiente de testes
- **Production**: Deploy automatizado

### CI/CD Pipeline
```
Git Push → Tests → Build → Security Scan → Deploy
```

### Monitoramento
- Métricas de performance
- Alertas de erro
- Health checks automáticos

## Roadmap Técnico

### Fase 1 (Atual)
- [x] Scaffold básico do monorepo
- [x] Estrutura de módulos educacionais
- [x] Interface web básica
- [ ] CLI funcional

### Fase 2
- [ ] Integração real com LLMs
- [ ] Sistema de autenticação
- [ ] Analytics de aprendizagem

### Fase 3
- [ ] Fine-tuning de modelos
- [ ] Personalização avançada
- [ ] Mobile app

## Considerações de Performance

### Frontend
- Static Site Generation (SSG) para conteúdo
- Code splitting por módulo
- Lazy loading de componentes

### Backend
- Connection pooling
- Query optimization
- Async processing

### LLM Integration
- Request batching
- Response caching
- Circuit breakers

## Padrões de Código

### TypeScript/JavaScript
- ESLint + Prettier
- Husky para pre-commit hooks
- Jest para testes unitários

### Python
- Black para formatação
- Pylint para linting
- pytest para testes

### Documentação
- JSDoc para código JavaScript
- Sphinx para código Python
- Markdown para documentação geral