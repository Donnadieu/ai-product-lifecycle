from typing import Dict, Any, Optional
import os
from enum import Enum
from google.generativeai import GenerativeModel
import google.generativeai as genai
from openai import OpenAI
import requests

class LLMProvider(str, Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    GEMINI = "gemini"

class LLMConfig:
    def __init__(self, provider: str = None, api_key: Optional[str] = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "openai")
        self.api_key = api_key or self._get_api_key()
        self._setup_client()

    def _get_api_key(self) -> str:
        if self.provider == LLMProvider.OPENAI:
            return os.getenv("OPENAI_API_KEY", "")
        elif self.provider == LLMProvider.DEEPSEEK:
            return os.getenv("DEEPSEEK_API_KEY", "")
        elif self.provider == LLMProvider.GEMINI:
            return os.getenv("GOOGLE_API_KEY", "")
        return ""

    def _setup_client(self):
        if self.provider == LLMProvider.GEMINI:
            genai.configure(api_key=self.api_key)
            self.client = GenerativeModel('gemini-pro')
        elif self.provider == LLMProvider.OPENAI:
            self.client = OpenAI(api_key=self.api_key)
        elif self.provider == LLMProvider.DEEPSEEK:
            self.base_url = "https://api.deepseek.com/v1"
            self.client = None  # We'll use requests directly for Deepseek

    def get_config(self, temperature: float = 0.7) -> Dict[str, Any]:
        """Get the configuration for autogen based on the provider"""
        if self.provider == LLMProvider.OPENAI:
            return {
                "llm_config": {
                    "config_list": [{
                        "model": "gpt-3.5-turbo",
                        "temperature": temperature,
                        "api_key": self.api_key
                    }]
                }
            }
        elif self.provider == LLMProvider.GEMINI:
            return {
                "llm_config": {
                    "config_list": [{
                        "model": "gemini-pro",
                        "temperature": temperature,
                        "api_key": self.api_key
                    }]
                }
            }
        elif self.provider == LLMProvider.DEEPSEEK:
            return {
                "llm_config": {
                    "config_list": [{
                        "model": "deepseek-chat",
                        "temperature": temperature,
                        "api_key": self.api_key,
                        "base_url": "https://api.deepseek.com/v1"
                    }],
                    "use_deepseek": True
                }
            }
        return {}

    async def generate_response(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate a response using the configured LLM provider"""
        try:
            if self.provider == LLMProvider.OPENAI:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )
                return response.choices[0].message.content

            elif self.provider == LLMProvider.GEMINI:
                response = self.client.generate_content(prompt)
                return response.text

            elif self.provider == LLMProvider.DEEPSEEK:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": temperature
                    }
                )
                return response.json()["choices"][0]["message"]["content"]

        except Exception as e:
            raise Exception(f"Error generating response with {self.provider}: {str(e)}")

        return ""
