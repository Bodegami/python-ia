from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
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

carregador = TextLoader(file_path="GTB_platinum_Nov23.txt", encoding="utf-8")
documentos = carregador.load()


quebrador = CharacterTextSplitter(chunk_size=1000)
textos = quebrador.split_documents(documentos)
#print(textos)

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(textos, embeddings)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

pergunta = "Como devo proceder caso tenha um item comprado roubado"
resulta = qa_chain.invoke({"query": pergunta})