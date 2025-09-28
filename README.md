# MEGA - Medical Education with Generative AI

Uma plataforma educacional médica inteligente que utiliza IA generativa para personalizar o aprendizado e criar experiências educativas adaptativas.

## 🎯 Visão Geral

O MEGA combina pedagogia médica tradicional com tecnologia de IA avançada, oferecendo:

- **Aprendizagem Personalizada**: Conteúdo adaptado ao ritmo e necessidades individuais
- **IA Generativa Multi-LLM**: Integração com GPT, Gemini, Claude e outros modelos
- **Conteúdo Interativo**: Casos clínicos, quizzes adaptativos e simulações
- **Módulos Especializados**: Conteúdo organizado por especialidades médicas

## 📚 Módulos Disponíveis

### 🫀 Cardiologia e ECG
- **[ECG Básico](./content/modules/ecg-basics/)** - Fundamentos da eletrocardiografia (8h)
  - Princípios da eletrofisiologia cardíaca
  - Identificação de ondas, intervalos e segmentos
  - Reconhecimento de variações normais
  - Interpretação sistemática básica

- **[ECG Intermediário](./content/modules/ecg-intermediate/)** - Interpretação avançada (12h)
  - Bloqueios de condução complexos
  - Sinais de isquemia e infarto
  - Hipertrofias atriais e ventriculares
  - Correlação clínico-eletrocardiográfica

### ⚡ Arritmias
- **[Arritmias Básicas](./content/modules/arrhythmias-basics/)** - Fundamentos do diagnóstico (10h)
  - Classificação por origem anatômica
  - Mecanismos de formação das arritmias
  - Arritmias supraventriculares e ventriculares
  - Abordagem sistemática ao diagnóstico

### 🩸 Hemodinâmica
- **[Hemodinâmica Básica](./content/modules/hemodynamics-basics/)** - Fundamentos da função cardíaca (14h)
  - Princípios fundamentais da hemodinâmica
  - Interpretação de curvas pressóricas
  - Análise do ciclo cardíaco
  - Correlação com manifestações clínicas

## 🏗️ Arquitetura

### Monorepo Structure
```
MEGA/
├── apps/
│   └── web/                 # Interface Next.js
├── packages/
│   ├── cli/                 # CLI Python com Typer
│   ├── llm-orchestrator/    # Orquestração multi-LLM
│   └── content-engine/      # Processamento de conteúdo
├── content/
│   └── modules/            # Módulos educacionais
├── models/
│   └── finetune/           # Infraestrutura de fine-tuning
└── docs/                   # Documentação técnica
```

### Tecnologias
- **Frontend**: Next.js 14, TypeScript, React
- **Backend**: Node.js, Python
- **IA**: Multi-LLM (OpenAI, Gemini, Claude)
- **Conteúdo**: Markdown, YAML, JSON
- **CLI**: Python Typer
- **Build**: pnpm workspaces

## 🚀 Início Rápido

### Pré-requisitos
- Node.js 18+
- Python 3.8+
- pnpm

### Instalação
```bash
# Clone o repositório
git clone https://github.com/Drmcoelho/MEGA.git
cd MEGA

# Instalar dependências
pnpm install

# Instalar CLI Python
cd packages/cli && pip install -e . && cd ../..

# Executar aplicação web
pnpm --filter mega-web dev
```

### Comandos CLI
```bash
# Verificar versão
mega version

# Listar módulos disponíveis
mega ingest

# Ajuda
mega --help
```

## 📖 Usando a Plataforma

### Interface Web
1. **Página Inicial**: Visão geral dos módulos disponíveis
2. **Página de Módulos**: Lista detalhada com objetivos e pré-requisitos
3. **Navegação Intuitiva**: Acesso fácil ao conteúdo educacional

### CLI
O CLI oferece ferramentas para administradores e desenvolvedores:
- Ingestão e validação de conteúdo
- Geração de casos clínicos (futuro)
- Administração do sistema

## 🎓 Pedagogia

### Metodologias Ativas
- **Problem-Based Learning (PBL)**
- **Case-Based Learning (CBL)**  
- **Simulation-Based Learning**
- **Adaptive Learning**

### Recursos Educacionais
- Lições estruturadas em Markdown
- Quizzes interativos com feedback
- Casos clínicos simulados
- Avaliação formativa contínua

## 🤖 IA Generativa

### Multi-LLM Orchestrator
- Integração com múltiplos provedores
- Fallback automático entre modelos
- Otimização de custos e latência
- Prompts especializados para medicina

### Funcionalidades IA
- Tutoria inteligente 24/7
- Geração de conteúdo personalizado
- Feedback adaptatico em tempo real
- Análise de padrões de aprendizagem

## 🔄 Desenvolvimento

### Status Atual: v0.1.0 (MVP)
- ✅ Estrutura do monorepo
- ✅ Interface web básica  
- ✅ 4 módulos educacionais completos
- ✅ CLI funcional
- ✅ Documentação inicial

### Próximas Funcionalidades
- Sistema de autenticação
- Integração real com LLMs
- Fine-tuning de modelos
- Aplicativo mobile

Ver [roadmap completo](./docs/roadmap.md) para detalhes.

## 🤝 Contribuindo

Veja nosso [guia de contribuição](./TODO.txt) e:

1. Fork o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

- **Código**: MIT License
- **Conteúdo Educacional**: Creative Commons BY-NC 4.0

Ver [LICENSE-DRAFT.md](./LICENSE-DRAFT.md) para detalhes completos.

## 🏥 Aviso Médico

⚠️ **Importante**: Este conteúdo é destinado exclusivamente para fins educacionais. Não substitui orientação médica profissional, diagnóstico ou tratamento. Sempre consulte profissionais qualificados para decisões clínicas.

## 📞 Contato

- **Issues**: [GitHub Issues](https://github.com/Drmcoelho/MEGA/issues)
- **Discussões**: [GitHub Discussions](https://github.com/Drmcoelho/MEGA/discussions)
- **Documentação**: [docs/](./docs/)

---

**MEGA** - Transformando a educação médica com IA 🚀