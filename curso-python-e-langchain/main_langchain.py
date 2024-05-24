from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")


numero_de_dias = 7
numero_de_criancas = 2
atividade = "praia"

prompt = f"Crie um roteiro de viagem {numero_de_dias} dias, para uma família com {numero_de_criancas} crianças, que gostam de {atividade}"

print(prompt)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=apikey)

resposta = llm.invoke(prompt)

print(resposta.content)
