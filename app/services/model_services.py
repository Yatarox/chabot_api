# app/services/model_services.py
from openai import OpenAI
from app.core.config import Config

class ModelService:
    def __init__(self, config: Config):
        self.config = config
        self.client = self._build_client()

    def _build_client(self) -> OpenAI:
        kwargs = {
            "base_url": self.config.model_url,
            "api_key": self.config.api_key,
        }
        if self.config.provider == "openrouter":
            kwargs["default_headers"] = {
                "HTTP-Referer": "http://localhost",
                "X-Title": "MyApp",
            }
        return OpenAI(**kwargs)

    def health_check(self) -> bool:
        try:
            self.client.models.list()
            return True
        except Exception as e:
            print(f"Provider: {self.config.provider}")
            print(f"Model URL: {self.config.model_url}")
            print(f"Model name: {self.config.model_name}")
            print(f"Health check failed: {e}")
            return False
        
    def clean_prompt(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            return ""
        return " ".join(prompt.split())

    def generate_response(self, prompt: str) -> str:
        prompt = self.clean_prompt(prompt)
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()