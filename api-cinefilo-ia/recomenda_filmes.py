from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os
from filme import *

load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")

def indica_filmes(tema):

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.9,
        api_key=apikey)

    parser = JsonOutputParser(pydantic_object=Filme)

    prompt = PromptTemplate(
        template="""
        Você é um cinefilo com um grande conhecimento em filmes. 
        Quando um usuário informar um tema, retorne uma recomendação
        de 3 filmes baseados no tema informado.
        Haverá situações que o usuário vai informar uma cena do filme e
        você deve retornar os possiveis filmes que contenham essa cena.
        Devolva a resposta com 3 filmes no seguinte formato: {instrucoes_formato}
        """,

        input_variables=["pergunta"],
        partial_variables={"instrucoes_formato": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    resposta = chain.invoke({"pergunta": tema})
    return resposta