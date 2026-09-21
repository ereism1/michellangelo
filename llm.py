"""
llm.py — camada única de abstração de LLM do Jarvis (ADR-004).

Todo acesso a modelo de linguagem passa por aqui. Trocar de provedor
é trocar PROVEDOR_LLM no .env — nada mais no projeto muda.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Resposta:
    texto: str
    provedor: str
    modelo: str
    tempo_s: float


def _adapter_anthropic(mensagens: list[dict], temperatura: float, modelo: str) -> str:
    from anthropic import Anthropic

    cliente = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = cliente.messages.create(
        model=modelo,
        max_tokens=1024,
        temperature=temperatura,
        messages=mensagens,
    )
    return msg.content[0].text


def _adapter_openai(mensagens: list[dict], temperatura: float, modelo: str) -> str:
    from openai import OpenAI

    cliente = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = cliente.chat.completions.create(
        model=modelo,
        temperature=temperatura,
        messages=mensagens,
    )
    return resp.choices[0].message.content


def _adapter_google(mensagens: list[dict], temperatura: float, modelo: str) -> str:
    from google import genai

    cliente = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    prompt = "\n\n".join(m["content"] for m in mensagens)
    resp = cliente.models.generate_content(
        model=modelo,
        contents=prompt,
        config={"temperature": temperatura},
    )
    return resp.text


_ADAPTERS = {
    "anthropic": _adapter_anthropic,
    "openai": _adapter_openai,
    "google": _adapter_google,
}


def _modelo_padrao(provedor: str) -> str:
    return {
        "anthropic": os.getenv("ANTHROPIC_MODEL") or "claude-sonnet-4-5",
        "openai": os.getenv("OPENAI_MODEL") or "gpt-4o-mini",
        "google": os.getenv("GOOGLE_MODEL") or "gemini-2.0-flash",
    }[provedor]


def perguntar(
    mensagens: list[dict],
    temperatura: float = 0.7,
    provedor: str | None = None,
    modelo: str | None = None,
) -> Resposta:
    provedor = provedor or os.getenv("PROVEDOR_LLM", "google")
    if provedor not in _ADAPTERS:
        raise ValueError(f"Provedor '{provedor}' desconhecido. Use: {list(_ADAPTERS)}")

    modelo = modelo or _modelo_padrao(provedor)
    inicio = time.monotonic()
    try:
        texto = _ADAPTERS[provedor](mensagens, temperatura, modelo)
    except KeyError as e:
        raise RuntimeError(
            f"Chave de API faltando pro provedor '{provedor}': {e}. Confira o .env."
        ) from e
    return Resposta(texto, provedor, modelo, time.monotonic() - inicio)
