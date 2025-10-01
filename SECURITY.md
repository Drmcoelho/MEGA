# Política de Segurança

## Versões Suportadas

| Versão | Suporte          |
| ------ | ---------------- |
| 0.1.x  | :white_check_mark: |

## Reportando uma Vulnerabilidade

A segurança do projeto MEGA é levada a sério. Se você descobriu uma vulnerabilidade de segurança, por favor nos ajude mantendo-a confidencial até que possamos corrigi-la.

### Como Reportar

**NÃO** crie uma issue pública para vulnerabilidades de segurança.

Em vez disso, use um dos seguintes métodos:

1. **GitHub Security Advisories (Preferido)**
   - Vá para https://github.com/Drmcoelho/MEGA/security/advisories
   - Clique em "New draft security advisory"
   - Preencha os detalhes da vulnerabilidade

2. **Email Privado**
   - Envie um email para: [ADICIONAR EMAIL DE SEGURANÇA]
   - Use GPG para criptografar informações sensíveis

### O que incluir no relatório

- Descrição detalhada da vulnerabilidade
- Passos para reproduzir o problema
- Versões afetadas
- Possível impacto
- Sugestões de correção (se houver)

### Processo de Resposta

1. **Confirmação**: Confirmamos o recebimento em até 48 horas
2. **Análise**: Investigamos e validamos a vulnerabilidade em até 7 dias
3. **Correção**: Desenvolvemos e testamos uma correção
4. **Divulgação**: Publicamos a correção e divulgamos responsavelmente
5. **Créditos**: Damos crédito ao pesquisador (se desejar)

## Práticas de Segurança

### Secrets e Credenciais

- **NUNCA** commite secrets, API keys, senhas ou credenciais no código
- Use variáveis de ambiente para configurações sensíveis
- Utilize o arquivo `.env` (que está no `.gitignore`)
- Exemplo de configuração em `.env.example`

### Dependências

- Auditoria automática de dependências via Dependabot
- Atualizações de segurança são priorizadas
- Use `pip-audit` para verificar vulnerabilidades localmente:
  ```bash
  pip install pip-audit
  pip-audit -r requirements-dev.txt
  ```

### Code Review

- Todas as mudanças passam por revisão de código
- PRs de segurança requerem múltiplos revisores
- Análise automatizada via CodeQL e outras ferramentas

### Autenticação e Autorização

- Use OAuth 2.0 para autenticação com serviços externos
- Implemente rate limiting em APIs
- Valide e sanitize todas as entradas de usuário

### Dados Sensíveis

- Dados pessoais devem ser criptografados em repouso
- Use HTTPS para todas as comunicações
- Implemente logging que não exponha dados sensíveis

## Configurações de Segurança

### Variáveis de Ambiente Obrigatórias

```bash
# APIs Externas
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Logging
MEGA_LOG_LEVEL=INFO  # Nunca use DEBUG em produção

# Segurança
MEGA_ENABLE_RATE_LIMIT=true
MEGA_MAX_REQUESTS_PER_MINUTE=60
```

### Checklist de Segurança para Contribuidores

- [ ] Código não contém secrets hardcoded
- [ ] Dependências foram auditadas
- [ ] Inputs são validados e sanitizados
- [ ] Erros não expõem informações sensíveis
- [ ] Logs não contêm dados pessoais ou secrets
- [ ] Testes de segurança foram executados

## Ferramentas de Segurança

O projeto utiliza as seguintes ferramentas automatizadas:

- **CodeQL**: Análise estática de código (SAST)
- **Dependabot**: Auditoria de dependências
- **TruffleHog**: Detecção de secrets
- **Gitleaks**: Detecção de secrets
- **Trivy**: Scanner de vulnerabilidades
- **pip-audit**: Auditoria de pacotes Python

## Compliance

### Dados Pessoais

Este projeto pode processar dados educacionais. Certifique-se de:

- Obter consentimento apropriado
- Implementar direito ao esquecimento
- Permitir exportação de dados
- Minimizar coleta de dados

### Licenciamento

- Todo código deve seguir a licença do projeto
- Dependências devem ter licenças compatíveis
- Atribuições devem ser mantidas

## Recursos Adicionais

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

## Atualizações desta Política

Esta política de segurança pode ser atualizada periodicamente. Última atualização: 2024-10-01
