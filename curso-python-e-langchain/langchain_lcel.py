from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.globals import set_debug
from dotenv import load_dotenv
import os
from langchain_core.pydantic_v1 import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")

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

modelo_restaurantes = PromptTemplate.from_template(
    template="Sugira restaurantes populares entre locais em {cidade}."
)

modelo_cultural = PromptTemplate.from_template(
    template="Sugira atividades e locais culturais em {cidade}."
)

parte1 = modelo_cidade | llm | parseador
parte2 = modelo_restaurantes | llm | StrOutputParser()
parte3 = modelo_cultural | llm | StrOutputParser()

# print(modelo_cidade.invoke({"interesse": "praias"})) #imprime o template do modelo

# resultado = parte1.invoke({"interesse": "praias"})
# print(resultado)

cadeia = (parte1 | parte2 | parte3)
resultado = cadeia.invoke({"interesse": "praias"})
print(resultado)