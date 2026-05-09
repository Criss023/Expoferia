# 🔍 Truth Verifier — Expoferia Compiladores

Verificador de veracidad de enunciados con arquitectura tipo compilador en 4 fases + fallback IA.

## Arquitectura

```
Entrada: "El sol gira alrededor de la tierra"
        │
        ▼
┌───────────────────────────────────────────────────┐
│  FASE 1: ANÁLISIS LÉXICO                          │
│  Tokeniza el enunciado e identifica cada palabra  │
│  → [NOMBRE_PROPIO: El sol] [VERBO: gira] ...      │
└──────────────────────┬────────────────────────────┘
                       │
        ▼
┌───────────────────────────────────────────────────┐
│  FASE 2: ANÁLISIS SINTÁCTICO                      │
│  Valida estructura: sujeto + verbo + predicado    │
│  → tipo: DECLARATIVO, sujeto: sol, verbo: gira    │
└──────────────────────┬────────────────────────────┘
                       │
        ▼
┌───────────────────────────────────────────────────┐
│  FASE 3: ANÁLISIS SEMÁNTICO                       │
│  Aplica reglas de la base de conocimiento         │
│  ¿Puede resolver? → Sí → FALSO (con 90% conf.)   │
│                  → No → pasa a Fase 4             │
└──────────────────────┬────────────────────────────┘
                       │ (solo si no pudo resolver)
        ▼
┌───────────────────────────────────────────────────┐
│  FASE 4: FALLBACK IA (Claude Sonnet)              │
│  La IA evalúa el enunciado con contexto amplio   │
│  → VERDADERO / FALSO / NO_VERIFICABLE             │
└───────────────────────────────────────────────────┘

Resultado: FALSO (por regla) o 🤖 FALSO (por IA)
```

## Veredictos posibles
| Icono | Veredicto | Descripción |
|-------|-----------|-------------|
| ✓ | VERDADERO | El enunciado es correcto |
| ✗ | FALSO | El enunciado es incorrecto |
| ⚠ | INDETERMINADO | Las reglas no pudieron decidir |
| — | NO VERIFICABLE | No puede verificarse objetivamente |
| 🤖 | (via IA) | Determinado por Claude |

---

## Setup

### 1. Backend (Python + FastAPI)

```bash
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate      # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Edita .env y pon tu ANTHROPIC_API_KEY

# Correr el servidor
uvicorn main:app --reload --port 8000
```

El backend queda en: http://localhost:8000

### 2. Frontend (React + Vite)

```bash
cd frontend

# Instalar dependencias
npm install

# Correr en desarrollo
npm run dev
```

El frontend queda en: http://localhost:5173

---

## Obtener API Key de Anthropic (gratis para pruebas)

1. Ve a https://console.anthropic.com
2. Crea una cuenta
3. Ve a "API Keys" y crea una nueva
4. Copia la key al archivo `backend/.env`

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

> **Nota:** Sin API key, el sistema sigue funcionando con las reglas base.
> Solo la Fase 4 no estará disponible.

---

## Estructura del proyecto

```
truth-verifier/
├── backend/
│   ├── main.py                 ← FastAPI app principal
│   ├── requirements.txt
│   ├── .env.example
│   └── analyzer/
│       ├── lexical.py          ← Fase 1: Tokenización
│       ├── syntactic.py        ← Fase 2: Estructura gramatical
│       ├── semantic.py         ← Fase 3: Reglas de veracidad
│       └── ai_fallback.py      ← Fase 4: Fallback Claude API
└── frontend/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── App.jsx             ← App principal
        ├── index.css
        └── components/
            ├── PhaseCard.jsx   ← Visualiza cada fase
            └── VerdictBanner.jsx ← Muestra el resultado final
```
