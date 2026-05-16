"""
FASE 4: FALLBACK IA
Cuando las reglas no pueden determinar la veracidad,
se llama a la API de Groq (Llama) para evaluarlo.
"""

import json
import os
import urllib.request
import urllib.error

PROMPT = """Eres un verificador de hechos preciso y conciso.
Tu única tarea es analizar si un enunciado es VERDADERO, FALSO o NO_VERIFICABLE.

Responde ÚNICAMENTE con un objeto JSON con esta estructura exacta:
{
  "verdict": "VERDADERO" | "FALSO" | "NO_VERIFICABLE",
  "confidence": número entre 0.0 y 1.0,
  "explanation": "Una explicación breve en español (máximo 2 oraciones)"
}

Reglas:
- VERDADERO: El enunciado es factualmente correcto según el conocimiento establecido.
- FALSO: El enunciado es factualmente incorrecto.
- NO_VERIFICABLE: No es posible verificarlo (opiniones, predicciones, enunciados ambiguos).
- NO incluyas texto fuera del JSON. No uses markdown. Solo el JSON puro."""


def ai_fallback(sentence: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return {
            "verdict": "NO_VERIFICABLE",
            "confidence": 0.0,
            "method": "IA_ERROR",
            "explanation": "No se configuró la API key. Agrega GROQ_API_KEY en el archivo .env",
            "needs_ai": False
        }

    payload = json.dumps({
      "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": f"Verifica este enunciado: \"{sentence}\""}
        ],
        "temperature": 0.1,
        "max_tokens": 256
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))

        raw_text = data["choices"][0]["message"]["content"].strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw_text)

        return {
            "verdict": result.get("verdict", "NO_VERIFICABLE"),
            "confidence": result.get("confidence", 0.5),
            "method": "IA_GROQ",
            "explanation": result.get("explanation", "La IA no proporcionó explicación."),
            "needs_ai": False
        }

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else "sin detalle"
        return {
            "verdict": "NO_VERIFICABLE",
            "confidence": 0.0,
            "method": "IA_ERROR",
            "explanation": f"HTTP {e.code}: {body[:200]}",
            "needs_ai": False
        }
    except json.JSONDecodeError:
        return {
            "verdict": "NO_VERIFICABLE",
            "confidence": 0.0,
            "method": "IA_ERROR",
            "explanation": "La IA respondió en un formato inesperado.",
            "needs_ai": False
        }
    except Exception as e:
        return {
            "verdict": "NO_VERIFICABLE",
            "confidence": 0.0,
            "method": "IA_ERROR",
            "explanation": f"Error: {str(e)}",
            "needs_ai": False
        }