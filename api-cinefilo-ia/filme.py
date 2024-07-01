from langchain_core.pydantic_v1 import BaseModel, Field

class Filme(BaseModel):
    titulo: str = Field(description="titulo do filme")
    descricao: str = Field(description="descricao do filme")
    duracao: int = Field(description="tempo de duracao em minutos")