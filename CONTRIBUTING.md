
# Guia de Contribuição para o Projeto MEGA

Ficamos felizes com o seu interesse em contribuir! Para garantir um desenvolvimento coeso e de alta qualidade, por favor, siga estas diretrizes.

## Começando

Antes de começar, certifique-se de que você configurou o ambiente de desenvolvimento localmente. As instruções completas estão no nosso [README.md](./README.md).

## Workflow de Contribuição

1.  **Faça um Fork do Repositório:** Comece criando um fork do repositório principal para a sua conta do GitHub.

2.  **Crie uma Branch:** Para cada nova feature ou correção de bug, crie uma branch descritiva a partir da branch `main`.
    ```bash
    git checkout -b minha-nova-feature
    ```

3.  **Desenvolva:** Faça as suas alterações no código.

4.  **Garanta a Qualidade do Código:** Antes de submeter sua contribuição, rode todas as verificações de qualidade e testes para garantir que nada foi quebrado.
    ```bash
    # Para verificar o código Python
    ./scripts/quality.sh

    # Para verificar o código Frontend
    pnpm --filter mega-web lint
    pnpm test
    ```

5.  **Faça o Commit:** Escreva uma mensagem de commit clara e concisa.
    ```bash
    git commit -m "feat: Adiciona nova funcionalidade X"
    ```

6.  **Envie as Alterações:** Faça o push da sua branch para o seu fork.
    ```bash
    git push origin minha-nova-feature
    ```

7.  **Abra um Pull Request:** Vá para o repositório original no GitHub e abra um Pull Request. Descreva as suas alterações em detalhes.

## Padrões de Código

-   **Formatação:** Utilizamos `Ruff` para Python e `Prettier` para o Frontend. O workflow de CI irá falhar se o código não estiver formatado corretamente. Rode os formatadores antes de fazer o commit:
    ```bash
    # Formatar Python
    ruff format .

    # Formatar Frontend
    pnpm --filter mega-web format
    ```

-   **Linting:** Utilizamos `Ruff` para Python e `ESLint` para o Frontend. O código deve passar em todas as verificações de lint.

-   **Testes:** Todo novo código deve, idealmente, ser acompanhado de testes. O CI executará todos os testes e não permitirá o merge se algum deles falhar.

Obrigado por contribuir para o MEGA!
