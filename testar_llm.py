from llm import perguntar

PERGUNTA = [{"role": "user", "content": "Diga 'oi' em uma frase curta."}]

if __name__ == "__main__":
    for provedor in ("google", "anthropic", "openai"):
        print(f"\n--- {provedor} ---")
        try:
            r = perguntar(PERGUNTA, provedor=provedor)
            print(f"OK ({r.tempo_s:.1f}s, {r.modelo}): {r.texto}")
        except Exception as e:
            print(f"FALHOU: {e}")
