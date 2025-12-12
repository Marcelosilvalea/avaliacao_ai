import os
from dotenv import load_dotenv
import google_genai as genai  # CORRETO!

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("❌ GEMINI_API_KEY não encontrada no arquivo .env")

        # Configuração do cliente
        self.client = genai.Client(api_key=self.api_key)

    def gerar_conteudo(self, prompt: str, temperatura: float = 0.9) -> str:
        response = self.client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            generation_config={"temperature": temperatura}
        )

        return response.text
