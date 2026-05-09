"""
FASE 3: ANÁLISIS SEMÁNTICO
Base de conocimiento con reglas para verificar la veracidad de enunciados.
Si no puede determinar → retorna INDETERMINADO para pasar al fallback de IA.
"""

import re
import math

# ─────────────────────────────────────────────
# BASE DE CONOCIMIENTO
# ─────────────────────────────────────────────

TRUE_FACTS = [
    # Astronomía
    r"(tierra|la tierra).*(orbita|gira alrededor).*(sol)",
    r"(sol).*(estrella)",
    r"(luna).*(satélite).*(tierra|natural)",
    r"(tierra).*(planeta)",
    r"(sol).*(centro).*(sistema solar)",
    r"(plutón).*(planeta enano)",
    r"(sistema solar).*(8|ocho).*(planetas)",

    # Ciencia
    r"(agua).*(h2o|hidrógeno|oxígeno)",
    r"(oxígeno).*(o2)",
    r"(luz).*(viaja|viaje|viajó).*(más rápido|velocidad)",
    r"(dna|adn).*(doble hélice)",
    r"(fotosíntesis).*(plantas|luz solar|clorofila)",
    r"(einstein).*(relatividad)",
    r"(newton).*(gravedad|gravitación)",
    r"(darwin).*(evolución|selección natural)",

    # Geografía
    r"(everest).*(montaña más alta|pico más alto)",
    r"(amazonas).*(río más largo|largo del mundo)",
    r"(pacífico).*(océano más grande)",
    r"(africa).*(continente)",
    r"(brasil).*(país más grande).*(sudamérica|latinoamérica)",
    r"(guatemala).*(país).*(centroamérica|centroamericano)",
    r"(ciudad de guatemala|guatemala city).*(capital).*(guatemala)",

    # Historia
    r"(colon|colón).*(llegó|descubrió).*(america|1492)",
    r"(segunda guerra mundial).*(1939|1945)",
    r"(primera guerra mundial).*(1914|1918)",
    r"(estados unidos).*(independencia).*(1776)",

    # Biología
    r"(humanos|seres humanos).*(mamíferos)",
    r"(ballena).*(mamífero)",
    r"(murciélago).*(mamífero)",
    r"(corazón humano).*(cuatro|4).*(cámaras|cavidades)",
    r"(humano).*(206|doscientos seis).*(huesos)",

    # Matemáticas básicas se resuelven por código
]

FALSE_FACTS = [
    # Astronomía (los clásicos errores)
    r"(sol).*(gira|orbita).*(tierra)",
    r"(tierra).*(plana|es plana|plano)",
    r"(sol).*(planeta)",
    r"(luna).*(estrella)",

    # Ciencia
    r"(einstein).*(reprobó|reprobó|jalado).*(matemáticas)",  # Mito famoso

    # Geografía
    r"(nilo).*(río más largo).*(mundo)",  # Debatido pero comúnmente considerado falso
    r"(australia).*(continente más grande)",

    # Biología
    r"(humano).*(10.*(cerebro|mente))",  # Mito del 10% del cerebro
]


def evaluate_math(sentence: str) -> dict | None:
    """Evalúa expresiones matemáticas simples."""
    # Patrón: "X operador Y = Z" o "X operador Y es Z"
    match = re.search(
        r'(\d+(?:[.,]\d+)?)\s*'
        r'([\+\-\*\/]|más|menos|por|entre|dividido entre|dividido por|elevado a)\s*'
        r'(\d+(?:[.,]\d+)?)\s*'
        r'(?:=|es igual a|es|son|igual a|equivale a)\s*'
        r'(\d+(?:[.,]\d+)?)',
        sentence, re.IGNORECASE
    )
    if not match:
        return None

    a = float(match.group(1).replace(',', '.'))
    op = match.group(2).strip().lower()
    b = float(match.group(3).replace(',', '.'))
    claimed = float(match.group(4).replace(',', '.'))

    op_map = {
        '+': a + b, 'más': a + b,
        '-': a - b, 'menos': a - b,
        '*': a * b, 'por': a * b,
        '/': a / b if b != 0 else None,
        'entre': a / b if b != 0 else None,
        'dividido entre': a / b if b != 0 else None,
        'dividido por': a / b if b != 0 else None,
        'elevado a': a ** b,
    }

    actual = op_map.get(op)
    if actual is None:
        return None

    is_true = abs(actual - claimed) < 0.0001
    return {
        "is_math": True,
        "actual_result": actual,
        "claimed_result": claimed,
        "verdict": "VERDADERO" if is_true else "FALSO",
        "confidence": 1.0,
        "explanation": f"{a} {op} {b} = {actual}, no {claimed}" if not is_true else f"{a} {op} {b} = {actual} ✓"
    }


def semantic_analysis(sentence: str, has_negation: bool) -> dict:
    """
    Verifica la veracidad del enunciado con reglas predefinidas.
    """
    sentence_lower = sentence.lower()

    # 1. Intentar evaluación matemática
    math_result = evaluate_math(sentence)
    if math_result:
        return {
            "verdict": math_result["verdict"],
            "confidence": math_result["confidence"],
            "method": "REGLA_MATEMATICA",
            "explanation": math_result["explanation"],
            "rule_matched": "Operación aritmética",
            "needs_ai": False
        }

    # 2. Buscar en hechos verdaderos
    for pattern in TRUE_FACTS:
        if re.search(pattern, sentence_lower):
            verdict = "FALSO" if has_negation else "VERDADERO"
            return {
                "verdict": verdict,
                "confidence": 0.90,
                "method": "REGLA_BASE_CONOCIMIENTO",
                "explanation": f"El enunciado {'contradice' if has_negation else 'coincide con'} un hecho establecido en la base de conocimiento.",
                "rule_matched": pattern,
                "needs_ai": False
            }

    # 3. Buscar en hechos falsos
    for pattern in FALSE_FACTS:
        if re.search(pattern, sentence_lower):
            verdict = "VERDADERO" if has_negation else "FALSO"
            return {
                "verdict": verdict,
                "confidence": 0.90,
                "method": "REGLA_BASE_CONOCIMIENTO",
                "explanation": f"El enunciado {'corrige' if has_negation else 'afirma'} algo que la base de conocimiento marca como incorrecto.",
                "rule_matched": pattern,
                "needs_ai": False
            }

    # 4. No se pudo determinar → necesita IA
    return {
        "verdict": "INDETERMINADO",
        "confidence": 0.0,
        "method": "SIN_REGLA",
        "explanation": "No se encontró una regla que pueda verificar este enunciado.",
        "rule_matched": None,
        "needs_ai": True
    }
