import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
apikey = os.getenv("GOOGLE_API_KEY")

def busca_filmes(descricao_da_cena):

  genai.configure(api_key=apikey)

  generation_config = {
    "temperature": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    system_instruction="""
      Você é um cinefilo com um grande conhecimento em filmes.    
      Sua responsabilidade e buscar filmes que se encaixem na descrição que o usuário informar.      
      Quando for responder o usuário, responda com uma LISTA de até 5 filmes correspondentes.
    """
  )

  chat = model.start_chat()
  response = chat.send_message(descricao_da_cena)

  return response.text
