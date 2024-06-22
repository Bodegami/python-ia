from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.globals import set_debug
from dotenv import load_dotenv
import os
from langchain_core.pydantic_v1 import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from operator import itemgetter

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")
set_debug(True)

class Destino(BaseModel):
    cidade = Field("cidade a visitar")
    motivo = Field("motivo pelo qual é intessante visitar")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=apikey)

parseador = JsonOutputParser(pydantic_object=Destino)

modelo_cidade = PromptTemplate(
    template="""Sugira uma cidade dado o meu interesse por {interesse}.
    {formatacao_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formatacao_de_saida": parseador.get_format_instructions()}
)

modelo_restaurantes = ChatPromptTemplate.from_template(
    template="Sugira restaurantes populares entre locais em {cidade}."
)

modelo_cultural = ChatPromptTemplate.from_template(
    template="Sugira atividades e locais culturais em {cidade}."
)

modelo_final = ChatPromptTemplate.from_messages(
    [
    ("ai", "Sugestão de viagem para a cidade: {cidade}"),
    ("ai", "Restaurantes que você não pode perder: {restaurantes}"),
    ("ai", "Atividades e locais culturais recomendados: {locais_culturais}"),
    ("system", "Combine as informações anteriores em 2 parágrafos coerentes")
    ])

parte1 = modelo_cidade | llm | parseador
parte2 = modelo_restaurantes | llm | StrOutputParser()
parte3 = modelo_cultural | llm | StrOutputParser()
parte4 = modelo_final | llm | StrOutputParser()

cadeia = (parte1 | { 
    "restaurantes": parte2, 
    "locais_culturais": parte3,
    "cidade": itemgetter("cidade") # a parte4 precida da cidade que está na resposta da parte1, utilizamos o itemgetter p/ recuperar essa informação
    }
    | parte4) # dessa forma, o resultado da parte1 é usado como input p/ parte 2 e 3


resultado = cadeia.invoke({"interesse": "praias"})
print(resultado)