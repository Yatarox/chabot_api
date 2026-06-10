import os

class Config:
    provider: str = os.getenv("PROVIDER", "local")
    if provider not in ["local", "openrouter"]:
        raise ValueError("Invalid provider specified. Must be 'local' or 'openrouter'.")
    if provider == "openrouter" and not os.getenv("api_key"):
        raise ValueError("api_key is required for OpenRouter provider. 667")
    if provider == "openrouter":
        openrouter_model_url: str = "https://openrouter.ai/api/v1"
        openrouter_api_key: str = os.getenv("api_key", "")
        openrouter_model_name: str = os.getenv("MODEL_NAME", "mistralai/mistral-7b-instruct")
    if provider == "local":
        local_model_url: str = os.getenv("MODEL_URL", "http://model:8000/v1")
        local_api_key: str = os.getenv("api_key", "dummy")
        local_model_name: str = os.getenv("MODEL_NAME", "HuggingFaceTB/SmolLM2-135M-Instruct")

    # OpenRouter
   

    @property
    def model_url(self) -> str:
        return self.openrouter_model_url if self.provider == "openrouter" else self.local_model_url

    @property
    def api_key(self) -> str:
        return self.openrouter_api_key if self.provider == "openrouter" else self.local_api_key

    @property
    def model_name(self) -> str:
        return self.openrouter_model_name if self.provider == "openrouter" else self.local_model_name