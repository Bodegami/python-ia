from langchain_openai import ChatOpenAI

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.globals import set_debug
from dotenv import load_dotenv
import os

load_dotenv()
apikey = os.getenv("OPENAI_API_KEY")
set_debug(True)

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=apikey)

carregadores = [
    PyPDFLoader("GTB_standard_Nov23.pdf"),
    PyPDFLoader("GTB_platinum_Nov23.pdf"),
    PyPDFLoader("GTB_gold_Nov23.pdf"),
    PyPDFLoader("GTB_black_Nov23.pdf")
]

documentos = []
for carregador in carregadores:
    documentos.extend(carregador.load())

quebrador = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
textos = quebrador.split_documents(documentos)
#print(textos)

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(textos, embeddings)

qa_chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

pergunta = "Como devo proceder caso tenha um item comprado roubado"
resulta = qa_chain.invoke({"query": pergunta})