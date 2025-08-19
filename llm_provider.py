import os
from typing import Protocol

# OpenAI
from openai import OpenAI

# Google Gemini
import google.generativeai as genai

# LangChain HF endpoint
from langchain_huggingface import HuggingFaceEndpoint


class LLM(Protocol):
    def generate(self, prompt: str) -> str: ...


class OpenAILLM:
    def __init__(self, model: str | None = None, api_key: str | None = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate(self, prompt: str) -> str:
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are a concise assistant."},
                      {"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()


class GoogleLLM:
    def __init__(self, model: str | None = None, api_key: str | None = None):
        genai.configure(api_key=api_key or os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(model or os.getenv("GOOGLE_MODEL", "gemini-1.5-pro"))

    def generate(self, prompt: str) -> str:
        resp = self.model.generate_content(prompt)
        return resp.text.strip()


class HFLLM:
    def __init__(self, repo_id: str | None = None, token: str | None = None):
        repo = repo_id or os.getenv("HF_REPO_ID", "mistralai/Mistral-7B-Instruct-v0.3")
        self.llm = HuggingFaceEndpoint(
            repo_id=repo,
            temperature=0.2,
            model_kwargs={
                "token": token or os.getenv("HF_TOKEN"),
                "max_length": "768",
            },
        )

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt)


def get_llm() -> LLM:
    provider = (os.getenv("LLM_PROVIDER") or "hf").lower()
    if provider == "openai":
        return OpenAILLM()
    if provider == "google":
        return GoogleLLM()
    return HFLLM()
