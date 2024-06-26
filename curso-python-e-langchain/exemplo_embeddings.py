from openai import OpenAI
client = OpenAI()

# Supondo que "descrição do quadrinho" seja a string de texto da descrição
descricao_quadrinho = "Aventuras épicas no espaço com heróis e vilões."

response = client.embeddings.create(
    input=descricao_quadrinho,
    model="text-embedding-3-small"
)

print(response.data[0].embedding)