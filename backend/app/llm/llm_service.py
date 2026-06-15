from groq import Groq
from app.config.settings import settings

class LLMService:
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.api_key = settings.GROQ_API_KEY
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")
            
        self.client = Groq(api_key=self.api_key)

    def generate_response(self, messages: list[dict[str, str]]) -> str:
        """
        Sends the formatted messages to the Groq API and returns the generated answer.
        """
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=0.2, # Keep it relatively deterministic for code facts
                max_tokens=2048,
            )
            return chat_completion.choices[0].message.content or ""
        except Exception as e:
            raise RuntimeError(f"Failed to generate response from Groq API: {str(e)}")
