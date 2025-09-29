# Template de Pull Request - MEGA

Use este template como referência para criar PRs bem estruturados e informativos.

## 📋 Objetivo

**Descreva claramente o objetivo desta pull request:**
- [ ] Nova funcionalidade
- [ ] Correção de bug
- [ ] Melhoria de performance
- [ ] Refatoração
- [ ] Documentação
- [ ] Configuração/Infraestrutura

## 🔄 Alterações

**Resumo das principais mudanças:**

### Arquivos Modificados
- `file1.py` - Descrição da alteração
- `file2.tsx` - Descrição da alteração
- `README.md` - Atualizações de documentação

### Funcionalidades Adicionadas
- Funcionalidade X com comportamento Y
- API endpoint `/api/nova-funcionalidade`
- Componente React `NovoComponente`

### Correções
- Fix no bug X que causava comportamento Y
- Correção de tipo no módulo Z

## 🧪 Teste Manual

**Comandos para testar as alterações:**

```bash
# Backend/Python
cd packages/nome-do-pacote
pytest tests/
python -m pytest test_specific.py

# Frontend/Web
cd apps/web
pnpm test
pnpm build
pnpm dev # Testar em localhost:3000

# CLI
mega comando --parametro valor
```

**Cenários de teste:**
1. [ ] Cenário 1: Descrição e resultado esperado
2. [ ] Cenário 2: Descrição e resultado esperado
3. [ ] Cenário 3: Teste de regressão

## ⚠️ Riscos e Considerações

**Possíveis impactos:**
- [ ] Breaking changes (documentar mitigação)
- [ ] Mudanças no banco de dados
- [ ] Alterações na API pública
- [ ] Dependências novas ou atualizadas

**Compatibilidade:**
- [ ] Backward compatible
- [ ] Requer migração
- [ ] Requer atualização de documentação

## 🔗 Próximos Passos

**Ações futuras relacionadas (se aplicável):**
- [ ] Issue #X a ser criada para follow-up
- [ ] Documentação adicional necessária
- [ ] Deploy em ambiente de staging
- [ ] Monitoramento pós-deploy

## 📚 Referências

**Links relacionados:**
- Issue: #numero
- Documentação: [link]
- Design/Figma: [link]
- Discussão prévia: [link]

---

### Checklist do Reviewer

**Para o revisor verificar:**
- [ ] Código segue padrões do projeto
- [ ] Testes adequados incluídos
- [ ] Documentação atualizada se necessário
- [ ] Performance considerada
- [ ] Segurança avaliada
- [ ] Logs apropriados para debug

### Comandos de Aprovação
```bash
# Executar antes de aprovar
pnpm install && pnpm build
pytest packages/
```