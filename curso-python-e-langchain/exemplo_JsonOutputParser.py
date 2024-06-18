from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.globals import set_debug

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")
set_debug(True)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=apikey)

# Defina a classe com a estrutura desejada
class Bandeira(BaseModel):
    pais: str = Field(description="nome do pais")
    cores: str = Field(description="cor principal da bandeira")
    historia: str = Field(description="história da bandeira")

# Defina a estrutura que será utilizada para processar a saída
parseador_bandeira = JsonOutputParser(pydantic_object=Bandeira)

prompt = PromptTemplate(
    template="Responda a pergunta do usuário.\n{instrucoes_formato}\n{pergunta}\n",
    input_variables=["pergunta"],
    partial_variables={"instrucoes_formato": parseador_bandeira.get_format_instructions()},
)

chain = prompt | llm | parseador_bandeira

resposta = chain.invoke({"pergunta": "Me fale da bandeira do Brasil"})
print(resposta)
