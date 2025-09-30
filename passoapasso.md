# **Roadmap Estratégico - Projeto ECGiga MEGA**

*Última Atualização: 29 de Setembro de 2025*

## Legenda de Ícones
- **💻 Feature:** Desenvolvimento de funcionalidade.
- **🚀 Deploy:** Lançamento de versão.
- **🧪 Teste:** Testes e garantia de qualidade.
- **🎨 Design:** UX/UI e experiência do usuário.
- **📚 Conteúdo:** Criação e gestão de material didático.
- **🧠 LLM:** Treinamento e orquestração de modelos de linguagem.
- **🏗️ Infra:** Infraestrutura e DevOps.
- **⚖️ Governança:** Licenciamento, documentação e comunidade.
- **⚡️ Otimização:** Melhoria de performance e refatoração.

---

## **Fase 1: MVP1 - Fundações, PWA e Conteúdo (Q4 2025)**

**Objetivo Principal:** Lançar uma PWA robusta e funcional, com conteúdo inicial de alta qualidade e suporte a múltiplos idiomas, estabelecendo uma base sólida para o crescimento.

### **Epic: Frontend & Progressive Web App (PWA)**
- 💻 **Setup Inicial:** Configurar `next-pwa` e bibliotecas associadas.
- 🎨 **Design Offline:** Projetar a UI para cenários sem conectividade (notificações, acesso a conteúdo em cache).
- 💻 **Manifesto:** Criar um `manifest.json` completo, com ícones, tela de splash e metadados para instalação.
- 💻 **Service Worker:** Implementar o registro, ciclo de vida e estratégias de cache (Cache First para assets, Stale-While-Revalidate para dados da API).
- 🧪 **Testes PWA:** Criar testes E2E (com Playwright/Cypress) para validar a funcionalidade offline e critérios de instalabilidade.

### **Epic: Internacionalização (i18n)**
- 💻 **Estrutura:** Integrar `next-intl` (ou similar) no `middleware.ts` e na estrutura de `pages`.
- 💻 **Refatoração:** Abstrair todo o texto visível na UI para arquivos de tradução (`messages/en.json`, `messages/pt.json`).
- 📚 **Tradução Inicial:** Realizar a tradução completa da interface e do conteúdo do módulo `ecg-basics`.

### **Epic: Conteúdo & Pedagogia**
- 📚 **Novos Módulos:**
    - Desenvolver conteúdo para "Síndromes Coronarianas Agudas (SCA)".
    - Desenvolver conteúdo para "Bloqueios de Ramo e Hemibloqueios".
- 📚 **Quizzes:** Criar bancos de questões (múltipla escolha, V/F) para os novos módulos, seguindo a estrutura dos `manifest.yaml`.
- 🎨 **Visualização:** Projetar e implementar componentes React para visualização interativa de traçados de ECG.

### **Epic: Infraestrutura & DevOps**
- 🏗️ **CI/CD (Frontend):** Configurar pipeline no `ci.yml` para build, lint, e testes a cada PR no `main`.
- 🏗️ **Deploy Automatizado:** Configurar Vercel (ou similar) para deploy contínuo do `apps/web`.
- 🏗️ **Analytics:** Integrar uma ferramenta de analytics (ex: Vercel Analytics, Plausible) para monitorar o uso.

### **Epic: Governança & Documentação**
- ⚖️ **Licença:** Finalizar a revisão do `LICENSE-DRAFT.md` e criar o arquivo `LICENSE` definitivo.
- ⚖️ **Contribuições:** Detalhar o processo de contribuição de código e conteúdo no `CONTRIBUTING.md`.
- 📖 **Documentação de Arquitetura:** Atualizar `docs/architecture.md` com as decisões tomadas nesta fase.

### **🚀 Deploy Alvo: `v0.1.0` - Beta Público**

---

## **Fase 2: MVP2 - Inteligência Adaptativa (Q1 2026)**

**Objetivo Principal:** Transformar la plataforma de conteúdo estático para uma experiência de aprendizado dinâmica e personalizada com a introdução do motor adaptativo.

### **Epic: Motor Adaptativo (`adaptive-engine`)**
- 💻 **API:** Desenvolver uma API robusta (usando FastAPI) para o motor, com endpoints para `getNextActivity`, `submitAnswer`, `getUserMastery`.
- 🧠 **Algoritmo:** Implementar o algoritmo de Knowledge Tracing ou similar para modelar a maestria do aluno.
- 🧪 **Testes do Motor:** Atingir >90% de cobertura de testes unitários e de integração para o `adaptive-engine`.
- 🏗️ **Containerização:** Criar um `Dockerfile` para o serviço do motor adaptativo.

### **Epic: Pipeline de LLM (`models/finetune`)**
- 🧠 **Dataset:** Definir e documentar o formato do dataset para fine-tuning de feedback pedagógico.
- 💻 **Preparação de Dados:** Implementar `prepare_dataset.py` para processar logs de interação e gerar o dataset de treino.
- 🧠 **Treinamento:** Executar os primeiros experimentos de fine-tuning com `train_lora.py` em um modelo base (ex: Llama 3, Mistral).
- 🧪 **Avaliação de Modelo:** Criar um script para avaliação qualitativa e quantitativa dos modelos fine-tuned.

### **Epic: Integração & Frontend**
- 💻 **Conexão API:** Integrar o frontend com a API do motor adaptativo.
- 🎨 **UI Adaptativa:** Projetar e implementar a UI que mostra o progresso de maestria e as recomendações do motor.
- 💻 **Geração de Casos:** Conectar o `case-generator` para fornecer cenários dinâmicos aos exercícios.

### **Epic: Infraestrutura & DevOps**
- 🏗️ **Deploy (Backend):** Configurar o deploy do motor adaptativo em um serviço escalável (ex: Google Cloud Run, AWS Fargate).
- 🏗️ **Orquestração:** Gerenciar a comunicação segura entre o frontend (Vercel) e o backend (Cloud).

### **🚀 Deploy Alvo: `v0.2.0` - Lançamento com Aprendizado Adaptativo**

---

## **Fase 3: MVP3 - Orquestração Multi-Agente (Q2 2026)**

**Objetivo Principal:** Alcançar um novo patamar de interatividade e inteligência através de uma arquitetura de múltiplos agentes de IA, capazes de realizar tarefas complexas.

### **Epic: Arquitetura Multi-Agente**
- 🧠 **Design:** Projetar a arquitetura de comunicação e responsabilidades entre os agentes (usando `llm-orchestrator`).
- 💻 **Agente de Avaliação:** Desenvolver um agente que utiliza um LLM fine-tuned para avaliar respostas abertas dos alunos.
- 💻 **Agente Pedagógico:** Criar um agente que fornece dicas, explicações e recursos adicionais com base no desempenho do aluno.
- 💻 **Agente Analista de ECG:** Investigar a viabilidade de um agente que interpreta imagens de ECG e gera relatórios.

### **Epic: Otimização e Escalabilidade**
- ⚡️ **Profiling:** Realizar profiling de performance de ponta a ponta, identificando gargalos.
- ⚡️ **Refatoração:** Otimizar componentes React, queries da API e lógica do motor adaptativo.
- 🧪 **Testes de Carga:** Implementar e executar testes de carga (k6, Locust) para simular centenas de usuários concorrentes.
- 🏗️ **Monitoramento Avançado:** Configurar monitoramento de performance de aplicação (APM) e logging estruturado.

### **🚀 Deploy Alvo: `v1.0.0` - Lançamento Oficial**
