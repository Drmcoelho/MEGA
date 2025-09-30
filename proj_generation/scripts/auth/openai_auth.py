# openai_auth.py

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente de um arquivo .env
load_dotenv()


def get_openai_api_key():
    """Obtém a chave da API da OpenAI a partir das variáveis de ambiente.

    A chave deve ser armazenada em um arquivo `.env` na raiz do projeto
    no formato:
    OPENAI_API_KEY='sua_chave_aqui'

    Returns:
        str: A chave da API da OpenAI.

    Raises:
        ValueError: Se a variável de ambiente OPENAI_API_KEY não for encontrada.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "A variável de ambiente OPENAI_API_KEY não foi encontrada. "
            "Por favor, crie um arquivo .env na raiz do projeto e adicione a chave."
        )
    return api_key


if __name__ == "__main__":
    # Exemplo de como usar a função
    try:
        print("Obtendo a chave da API da OpenAI...")
        api_key = get_openai_api_key()
        print("Chave da API da OpenAI obtida com sucesso!")
        # Em um uso real, você passaria essa chave para o cliente da OpenAI
        # from openai import OpenAI
        # client = OpenAI(api_key=api_key)
    except ValueError as e:
        print(e)
