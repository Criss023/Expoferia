import { useState } from 'react'
import PhaseStep from './components/PhaseCard'
import VerdictBanner from './components/VerdictBanner'

const EXAMPLES = [
  "La tierra gira alrededor del sol",
  "El sol gira alrededor de la tierra",
  "2 + 2 = 4",
  "El agua es H2O",
  "La tierra es plana",
  "Las ballenas son mamíferos",
  "Guatemala es un país de Centroamérica",
  "Einstein descubrió la gravedad",
]

const EMPTY_PHASES = [
  { phase: 1, name: 'Análisis Léxico',      status: 'pending', result: null },
  { phase: 2, name: 'Análisis Sintáctico',  status: 'pending', result: null },
  { phase: 3, name: 'Análisis Semántico',   status: 'pending', result: null },
  { phase: 4, name: 'Fallback IA (Groq · Llama)',          status: 'pending', result: null },
]

export default function App() {
  const [sentence, setSentence] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])

  async function verify(text) {
    const s = (text || sentence).trim()
    if (!s) return
    setSentence(s)
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch('/api/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sentence: s })
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setResult(data)
      setHistory(prev => [{ sentence: s, verdict: data.final_verdict }, ...prev.slice(0, 7)])
    } catch (e) {
      setError('No se pudo conectar con el backend. ¿Está corriendo en http://localhost:8000?')
    } finally {
      setLoading(false)
    }
  }

  const displayPhases = result ? result.phases : EMPTY_PHASES

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>

      {/* Header */}
      <header style={{
        background: 'var(--white)',
        borderBottom: '1px solid var(--border)',
        padding: '0 40px',
        height: '60px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{
            width: '30px', height: '30px', borderRadius: '8px',
            background: 'var(--text)', display: 'flex',
            alignItems: 'center', justifyContent: 'center',
            fontSize: '14px',
          }}>⊕</div>
          <span style={{
            fontFamily: 'var(--font-display)',
            fontSize: '17px', fontWeight: 600,
            color: 'var(--text)', letterSpacing: '-0.3px',
          }}>Truth Verifier</span>
        </div>
        <span style={{
          fontFamily: 'var(--font-body)', fontSize: '12px',
          color: 'var(--text-muted)', fontWeight: 400,
        }}>Compiladores · Expoferia</span>
      </header>

      {/* Main */}
      <div style={{ maxWidth: '860px', margin: '0 auto', padding: '48px 24px' }}>

        {/* Hero text */}
        <div style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 style={{
            fontFamily: 'var(--font-display)',
            fontSize: '42px', fontWeight: 700,
            color: 'var(--text)', letterSpacing: '-1px',
            lineHeight: 1.1, marginBottom: '12px',
          }}>
            ¿Es esto <em style={{ fontStyle: 'italic', fontWeight: 300 }}>verdad</em>?
          </h1>
          <p style={{
            fontFamily: 'var(--font-body)', fontSize: '15px',
            color: 'var(--text-muted)', fontWeight: 400,
          }}>
            Escribe un enunciado y lo analizamos en 4 fases como un compilador.
          </p>
        </div>

        {/* Input */}
        <div style={{
          background: 'var(--white)',
          border: '1.5px solid var(--border)',
          borderRadius: 'var(--radius)',
          padding: '6px 6px 6px 20px',
          display: 'flex', alignItems: 'center', gap: '10px',
          boxShadow: 'var(--shadow)',
          marginBottom: '16px',
          transition: 'border-color 0.2s, box-shadow 0.2s',
        }}
          onFocusCapture={e => e.currentTarget.style.borderColor = 'var(--text)'}
          onBlurCapture={e => e.currentTarget.style.borderColor = 'var(--border)'}
        >
          <input
            value={sentence}
            onChange={e => setSentence(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && verify()}
            placeholder="Ej: La tierra gira alrededor del sol..."
            style={{
              flex: 1, border: 'none', outline: 'none',
              background: 'transparent',
              fontFamily: 'var(--font-body)', fontSize: '15px',
              color: 'var(--text)', fontWeight: 400,
            }}
          />
          <button
            onClick={() => verify()}
            disabled={loading || !sentence.trim()}
            style={{
              padding: '11px 24px',
              background: loading || !sentence.trim() ? 'var(--surface)' : 'var(--text)',
              color: loading || !sentence.trim() ? 'var(--text-muted)' : 'white',
              border: 'none', borderRadius: '10px',
              fontFamily: 'var(--font-body)', fontSize: '14px', fontWeight: 600,
              cursor: loading || !sentence.trim() ? 'not-allowed' : 'pointer',
              transition: 'all 0.15s',
              whiteSpace: 'nowrap',
            }}
          >
            {loading ? 'Analizando...' : 'Verificar'}
          </button>
        </div>

        {/* Example chips */}
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '40px' }}>
          {EXAMPLES.map((ex, i) => (
            <button key={i} onClick={() => verify(ex)} style={{
              padding: '5px 13px', borderRadius: '100px',
              background: 'var(--white)', border: '1px solid var(--border)',
              color: 'var(--text-muted)', fontSize: '12px',
              fontFamily: 'var(--font-body)', cursor: 'pointer',
              transition: 'all 0.15s',
            }}
              onMouseEnter={e => { e.target.style.background = 'var(--surface)'; e.target.style.color = 'var(--text)' }}
              onMouseLeave={e => { e.target.style.background = 'var(--white)'; e.target.style.color = 'var(--text-muted)' }}
            >
              {ex}
            </button>
          ))}
        </div>

        {/* Error */}
        {error && (
          <div style={{
            background: 'var(--false-bg)', border: '1px solid var(--false-border)',
            borderRadius: 'var(--radius-sm)', padding: '14px 18px',
            fontFamily: 'var(--font-body)', fontSize: '13px',
            color: 'var(--false-color)', marginBottom: '24px',
          }}>⚠ {error}</div>
        )}

        {/* Loading */}
        {loading && (
          <div style={{ textAlign: 'center', padding: '60px 0' }}>
            <div style={{
              width: '40px', height: '40px', borderRadius: '50%',
              border: '2px solid var(--border)',
              borderTop: '2px solid var(--text)',
              margin: '0 auto 16px',
              animation: 'spin 0.8s linear infinite',
            }} />
            <p style={{ fontFamily: 'var(--font-body)', fontSize: '14px', color: 'var(--text-muted)' }}>
              Analizando enunciado...
            </p>
            <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
          </div>
        )}

        {/* Result layout */}
        {result && !loading && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 220px', gap: '20px', alignItems: 'start' }}>

            {/* Left: Verdict */}
            <VerdictBanner
              verdict={result.final_verdict}
              confidence={result.confidence}
              method={result.method}
              explanation={result.explanation}
              processingTime={result.processing_time_ms}
              sentence={result.sentence}
            />

            {/* Right: Phases stepper + history */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>

              {/* Phases */}
              <div style={{
                background: 'var(--white)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)',
                padding: '20px',
                boxShadow: 'var(--shadow)',
              }}>
                <p style={{
                  fontFamily: 'var(--font-body)', fontSize: '11px',
                  fontWeight: 600, color: 'var(--text-muted)',
                  letterSpacing: '0.08em', textTransform: 'uppercase',
                  marginBottom: '16px',
                }}>Fases del compilador</p>
                <div style={{ display: 'flex', flexDirection: 'column' }}>
                  {displayPhases.map((p, i) => (
                    <PhaseStep key={p.phase} {...p} index={i} visible={!!result} />
                  ))}
                </div>
              </div>

              {/* History */}
              {history.length > 0 && (
                <div style={{
                  background: 'var(--white)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius)',
                  padding: '20px',
                  boxShadow: 'var(--shadow)',
                }}>
                  <p style={{
                    fontFamily: 'var(--font-body)', fontSize: '11px',
                    fontWeight: 600, color: 'var(--text-muted)',
                    letterSpacing: '0.08em', textTransform: 'uppercase',
                    marginBottom: '12px',
                  }}>Recientes</p>
                  {history.map((h, i) => (
                    <div key={i} onClick={() => verify(h.sentence)} style={{
                      display: 'flex', justifyContent: 'space-between',
                      alignItems: 'flex-start', gap: '8px',
                      padding: '7px 0',
                      borderBottom: i < history.length - 1 ? '1px solid var(--border)' : 'none',
                      cursor: 'pointer',
                    }}>
                      <span style={{
                        fontFamily: 'var(--font-body)', fontSize: '11px',
                        color: 'var(--text-muted)', lineHeight: 1.4,
                        flex: 1,
                      }}>{h.sentence.length > 35 ? h.sentence.slice(0, 33) + '…' : h.sentence}</span>
                      <span style={{
                        fontSize: '11px', fontWeight: 700, flexShrink: 0,
                        color: h.verdict === 'VERDADERO' ? 'var(--true-color)'
                             : h.verdict === 'FALSO'     ? 'var(--false-color)'
                             : 'var(--unknown-color)',
                      }}>
                        {h.verdict === 'VERDADERO' ? '✓' : h.verdict === 'FALSO' ? '✗' : '?'}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Empty state */}
        {!result && !loading && !error && (
          <div style={{ textAlign: 'center', padding: '40px 0', color: 'var(--text-light)' }}>
            <p style={{ fontFamily: 'var(--font-display)', fontSize: '28px', fontWeight: 300, fontStyle: 'italic', marginBottom: '8px' }}>
              Todo listo
            </p>
            <p style={{ fontFamily: 'var(--font-body)', fontSize: '13px' }}>
              Escribe algo arriba o selecciona un ejemplo
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
