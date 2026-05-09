"""
FASE 2: ANÁLISIS SINTÁCTICO
Valida que el enunciado tenga una estructura gramatical válida.
Verifica: sujeto + verbo + predicado (mínimo viable)
"""

import re

# Patrones de estructura válidos para enunciados declarativos
VALID_PATTERNS = [
    # Sujeto + verbo copulativo + predicado: "El sol es una estrella"
    r'^(el|la|los|las|un|una|[A-ZÁÉÍÓÚÑ])\s+\w+\s+(es|son|fue|fueron|está|están)\s+.+$',
    # Sujeto + verbo de acción + complemento: "La tierra orbita el sol"
    r'^\w[\w\s]+\s+\w+(a|e|i|o|u)\s+.+$',
    # Enunciado matemático: "2 + 2 = 4" o "2 más 2 es 4"
    r'^\d+\s*[\+\-\*\/]\s*\d+\s*[=]\s*\d+$',
    r'^\d+\s+(más|menos|por|entre|dividido)\s+\d+\s+(es|son|igual|equivale)\s+\w+$',
    # Enunciado con "tiene": "El agua tiene dos átomos de hidrógeno"
    r'^.+(tiene|tienen|posee|poseen)\s+.+$',
]

# Indicadores de que NO es un enunciado declarativo
QUESTION_INDICATORS = ["?", "¿"]
COMMAND_INDICATORS = ["!", "¡"]


def syntactic_analysis(sentence: str, tokens: list) -> dict:
    """
    Analiza la estructura sintáctica del enunciado.
    """
    sentence_clean = sentence.strip()

    issues = []
    warnings = []

    # 1. Verificar que no sea pregunta o comando
    if any(ind in sentence_clean for ind in QUESTION_INDICATORS):
        return {
            "valid": False,
            "structure_type": "PREGUNTA",
            "issues": ["El enunciado es una pregunta, no una afirmación verificable"],
            "warnings": [],
            "subject": None,
            "verb": None
        }

    if sentence_clean.endswith("!"):
        warnings.append("El enunciado es exclamativo, puede ser difícil de verificar")

    # 2. Verificar longitud mínima
    if len(tokens) < 2:
        return {
            "valid": False,
            "structure_type": "INCOMPLETO",
            "issues": ["El enunciado es demasiado corto para ser verificado"],
            "warnings": [],
            "subject": None,
            "verb": None
        }

    # 3. Identificar el verbo principal
    verb_token = next((t for t in tokens if t["type"] == "VERBO"), None)
    if not verb_token:
        warnings.append("No se identificó un verbo claro, el análisis puede ser menos preciso")

    # 4. Identificar el sujeto (primer nombre propio o sustantivo antes del verbo)
    subject_token = None
    for t in tokens:
        if t["type"] in ("NOMBRE_PROPIO", "SUSTANTIVO_O_ADJETIVO"):
            subject_token = t
            break
        if t["type"] == "VERBO":
            break

    if not subject_token:
        warnings.append("No se identificó claramente el sujeto del enunciado")

    # 5. Determinar el tipo de estructura
    structure_type = "DECLARATIVO"
    if re.match(r'^\d+\s*[\+\-\*\/\=]\s*\d+', sentence_clean):
        structure_type = "MATEMATICO"
    elif any(t["type"] == "NEGACION" for t in tokens):
        structure_type = "DECLARATIVO_NEGATIVO"
    elif any(t["value"].lower() in ("mayor", "menor", "más", "menos") for t in tokens):
        structure_type = "COMPARATIVO"

    return {
        "valid": len(issues) == 0,
        "structure_type": structure_type,
        "issues": issues,
        "warnings": warnings,
        "subject": subject_token["value"] if subject_token else None,
        "verb": verb_token["value"] if verb_token else None
    }
