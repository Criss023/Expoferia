"""
TRUTH VERIFIER - Backend principal
Expoferia - Compiladores
API REST con FastAPI que orquesta las 4 fases del compilador.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import time

from analyzer.lexical import lexical_analysis
from analyzer.syntactic import syntactic_analysis
from analyzer.semantic import semantic_analysis
from analyzer.ai_fallback import ai_fallback

load_dotenv()

app = FastAPI(
    title="Truth Verifier API",
    description="Verificador de veracidad de enunciados con análisis tipo compilador + IA",
    version="1.0.0"
)

# CORS para permitir peticiones desde el frontend de React/Vite
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class VerifyRequest(BaseModel):
    sentence: str


@app.get("/")
def root():
    return {"message": "Truth Verifier API activa 🔍", "version": "1.0.0"}


@app.post("/verify")
def verify(request: VerifyRequest):
    """
    Endpoint principal: recibe un enunciado y lo pasa por las 4 fases del compilador.
    """
    start_time = time.time()
    sentence = request.sentence.strip()

    if not sentence:
        return {"error": "El enunciado no puede estar vacío"}

    phases = []

    # ─────────────────────────────────────────
    # FASE 1: ANÁLISIS LÉXICO
    # ─────────────────────────────────────────
    lexical = lexical_analysis(sentence)
    phases.append({
        "phase": 1,
        "name": "Análisis Léxico",
        "description": "Tokenización e identificación de palabras",
        "status": "success" if lexical["valid"] else "error",
        "result": lexical
    })

    if not lexical["valid"]:
        return {
            "sentence": sentence,
            "phases": phases,
            "final_verdict": "NO_VERIFICABLE",
            "confidence": 0.0,
            "method": "ERROR_LEXICO",
            "explanation": "El enunciado no pudo ser tokenizado correctamente.",
            "processing_time_ms": round((time.time() - start_time) * 1000, 2)
        }

    # ─────────────────────────────────────────
    # FASE 2: ANÁLISIS SINTÁCTICO
    # ─────────────────────────────────────────
    syntactic = syntactic_analysis(sentence, lexical["tokens"])
    phases.append({
        "phase": 2,
        "name": "Análisis Sintáctico",
        "description": "Validación de estructura gramatical",
        "status": "success" if syntactic["valid"] else "warning",
        "result": syntactic
    })

    # Advertencias pero no bloqueante, continuamos de todas formas
    # solo bloqueamos si es pregunta
    if not syntactic["valid"] and syntactic["structure_type"] == "PREGUNTA":
        return {
            "sentence": sentence,
            "phases": phases,
            "final_verdict": "NO_VERIFICABLE",
            "confidence": 0.0,
            "method": "ERROR_SINTACTICO",
            "explanation": "El enunciado es una pregunta, no una afirmación verificable.",
            "processing_time_ms": round((time.time() - start_time) * 1000, 2)
        }

    # ─────────────────────────────────────────
    # FASE 3: ANÁLISIS SEMÁNTICO
    # ─────────────────────────────────────────
    semantic = semantic_analysis(sentence, lexical["has_negation"])
    phases.append({
        "phase": 3,
        "name": "Análisis Semántico",
        "description": "Verificación con base de conocimiento",
        "status": "success" if not semantic["needs_ai"] else "fallback",
        "result": semantic
    })

    # ─────────────────────────────────────────
    # FASE 4: FALLBACK IA (solo si es necesario)
    # ─────────────────────────────────────────
    if semantic["needs_ai"]:
        ai_result = ai_fallback(sentence)
        phases.append({
            "phase": 4,
            "name": "Fallback IA (Claude)",
            "description": "La IA evalúa el enunciado que las reglas no pudieron resolver",
            "status": "success" if ai_result["verdict"] != "IA_ERROR" else "error",
            "result": ai_result
        })

        final_verdict = ai_result["verdict"]
        confidence = ai_result["confidence"]
        method = ai_result["method"]
        explanation = ai_result["explanation"]
    else:
        phases.append({
            "phase": 4,
            "name": "Fallback IA (Claude)",
            "description": "No fue necesario — las reglas resolvieron el enunciado",
            "status": "skipped",
            "result": {"skipped": True}
        })
        final_verdict = semantic["verdict"]
        confidence = semantic["confidence"]
        method = semantic["method"]
        explanation = semantic["explanation"]

    processing_time = round((time.time() - start_time) * 1000, 2)

    return {
        "sentence": sentence,
        "phases": phases,
        "final_verdict": final_verdict,
        "confidence": confidence,
        "method": method,
        "explanation": explanation,
        "processing_time_ms": processing_time
    }
