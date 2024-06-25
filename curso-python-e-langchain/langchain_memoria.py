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

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=apikey)

mensagens = [
        "Quero visitar um lugar no Brasil famoso por suas praias e cultura. Pode me recomendar?",
        "Qual é o melhor período do ano para visitar em termos de clima?",
        "Quais tipos de atividades ao ar livre estão disponíveis?",
        "Alguma sugestão de acomodação eco-friendly por lá?",
        "Cite outras 20 cidades com características semelhantes às que descrevemos até agora. Rankeie por mais interessante, incluindo no meio ai a que você já sugeriu.",
        "Na primeira cidade que você sugeriu lá atrás, quero saber 5 restaurantes para visitar. Responda somente o nome da cidade e o nome dos restaurantes.",
]

longa_conversa = ""

for mensagem in mensagens:
    longa_conversa = f"Usuário: {mensagem}\n"
    longa_conversa += f"AI: "

    modelo = PromptTemplate(template=longa_conversa, 
                            input_variables=[""]) #O PromptTemplate sempre exige o input_variables
    cadeia = modelo | llm | StrOutputParser()
    resposta = cadeia.invoke(input={}) # O invoke sempre exige um dicionario
    #print(resposta)

    longa_conversa += resposta + "\n"
    print(longa_conversa)