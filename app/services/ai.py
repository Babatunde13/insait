from openai import OpenAI
from app.config import config
from app.logger import Logger

client = OpenAI(api_key=config.OPENAI_API_KEY)

class AIService:
    def __init__(self):
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.chat_completions = client.chat.completions
        self.logger = Logger("AIService")

    def generate_text(self, prompt):
        try:
            response = self.chat_completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            return response["choices"][0]["message"]["content"]
        except Exception as e:
            self.logger.error("Error generating text", {"error": str(e)})
            if config.USE_AI_MOCK:
                return "This is a mock response."
            return None

ai_service = AIService()
