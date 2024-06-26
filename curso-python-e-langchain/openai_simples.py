# Imports e carregando as variaveis de ambiente

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")

print(apikey)

# Lógica de negócio

numero_de_dias = 7
numero_de_criancas = 2
atividade = "praia"

prompt = f"Crie um roteiro de viagem {numero_de_dias} dias, para uma família com {numero_de_criancas} crianças, que gostam de {atividade}"

print(prompt)

cliente = OpenAI(api_key=apikey)

resposta = cliente.chat.completions.create(
    model="gpt-3.5-turbo",
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant"
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print(resposta.choices[0].message.content)