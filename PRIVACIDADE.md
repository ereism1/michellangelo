# PRIVACIDADE

Escrito de cabeça fria, no FDS 1 — não às 2h da manhã em janeiro.

## Nunca sai da máquina (ADR-009)

- Áudio bruto: transcrição é local, só o texto segue adiante
- Vídeo e imagem de câmera: reconhecimento facial roda local

## Nunca vira prompt / nunca vai pra API de LLM

- Senhas, tokens, chaves de API
- Números de documento
- Dados de terceiros sem consentimento deles
- Localização em tempo real
- (edite: o que mais é sensível pra você especificamente?)

## Pode ir pra API

- Conteúdo da conversa com o Jarvis
- Fatos não identificáveis sobre rotina, preferências e projetos

## Onde é aplicado

`llm.py` é o único portão de saída (ADR-004) — é onde um filtro automático
entraria no futuro. Hoje a disciplina é manual.
