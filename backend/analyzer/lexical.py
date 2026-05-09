"""
FASE 1: ANÁLISIS LÉXICO
Tokeniza el enunciado e identifica el tipo de cada token.
"""

import re

# Palabras clave que ayudan al análisis
STOPWORDS_ES = {"el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del",
                "al", "en", "con", "por", "para", "a", "y", "o", "pero", "que",
                "es", "son", "fue", "ser", "estar", "se", "su", "sus"}

VERBS_COMMON = {"es", "son", "fue", "fueron", "está", "están", "tiene", "tienen",
                "gira", "orbita", "produce", "contiene", "mide", "vale", "igual",
                "existe", "vive", "nació", "murió", "descubrió", "inventó"}

NEGATION_WORDS = {"no", "nunca", "jamás", "ni", "tampoco", "ningún", "ninguna"}

QUANTITY_WORDS = {"más", "menos", "mayor", "menor", "igual", "mayor", "menor",
                  "todos", "ninguno", "siempre", "nunca"}


class Token:
    def __init__(self, value: str, token_type: str, position: int):
        self.value = value
        self.token_type = token_type
        self.position = position

    def to_dict(self):
        return {
            "value": self.value,
            "type": self.token_type,
            "position": self.position
        }


def classify_token(word: str) -> str:
    """Clasifica un token según su tipo."""
    w = word.lower().strip(".,;:!?\"'")

    if re.match(r'^-?\d+([.,]\d+)?$', w):
        return "NUMERO"
    if w in NEGATION_WORDS:
        return "NEGACION"
    if w in VERBS_COMMON:
        return "VERBO"
    if w in STOPWORDS_ES:
        return "STOPWORD"
    if w in QUANTITY_WORDS:
        return "CANTIDAD"
    if re.match(r'^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+', word):  # Empieza con mayúscula
        return "NOMBRE_PROPIO"
    return "SUSTANTIVO_O_ADJETIVO"


def lexical_analysis(sentence: str) -> dict:
    """
    Realiza el análisis léxico del enunciado.
    Retorna los tokens encontrados y estadísticas básicas.
    """
    # Limpieza básica
    sentence = sentence.strip()
    if not sentence:
        return {"error": "Enunciado vacío", "tokens": [], "valid": False}

    # Tokenización simple por espacios y puntuación
    raw_tokens = re.findall(r'\b[\wáéíóúñÁÉÍÓÚÑ]+\b|\d+[.,]?\d*|[+\-*/=<>]', sentence)

    tokens = []
    for i, word in enumerate(raw_tokens):
        token_type = classify_token(word)
        tokens.append(Token(word, token_type, i).to_dict())

    # Detectar si hay negación
    has_negation = any(t["type"] == "NEGACION" for t in tokens)

    # Detectar números para enunciados matemáticos
    numbers = [t["value"] for t in tokens if t["type"] == "NUMERO"]

    return {
        "tokens": tokens,
        "token_count": len(tokens),
        "has_negation": has_negation,
        "numbers_found": numbers,
        "original_sentence": sentence,
        "valid": len(tokens) > 0
    }
