from openai import OpenAI
from dotenv import load_dotenv
import os

# DOCS
# https://platform.openai.com/docs/api-reference/chat/create

load_dotenv()
cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

modelo = "gpt-3.5-turbo"

prompt_sistema = """
    Você é um categorizador de produtos.
    Você deve assumir as categorias presentes na lista abaixo.

    # Lista de Categorias Válidas
    - Moda Sustentável
    - Produtos para o Lar
    - Beleza Natural
    - Eletrônicos Verdes

    # Formato da Saída
    Produto: Nome do Produto
    Categoria: apresente a categoria do produto

    # Exemplo de Saída
    Produto: Escova elétrica com recarga solar
    Categoria: Eletrônicos Verdes
    """


print("Informe um novo produto: ")
prompt_usuario = input()


resposta = cliente.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ],
    model=modelo,
    temperature=0.5,
    max_tokens=200  ,
    frequency_penalty=1.0,
    n = 1
)

# print(resposta)
print(resposta.choices[0].message.content)