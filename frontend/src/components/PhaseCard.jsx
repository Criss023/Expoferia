import { useState } from 'react'

const STATUS = {
  success:  { color: 'var(--true-color)',    dot: 'var(--true-soft)',    label: 'OK'      },
  warning:  { color: 'var(--unknown-color)', dot: 'var(--unknown-soft)', label: 'Aviso'   },
  error:    { color: 'var(--false-color)',   dot: 'var(--false-soft)',   label: 'Error'   },
  fallback: { color: 'var(--ai-color)',      dot: 'var(--ai-bg)',        label: 'IA'      },
  skipped:  { color: 'var(--text-light)',    dot: 'var(--border)',       label: 'Saltada' },
  pending:  { color: 'var(--text-light)',    dot: 'var(--border)',       label: '...'     },
}

export default function PhaseStep({ phase, name, status, result, index, visible }) {
  const [open, setOpen] = useState(false)
  const cfg = STATUS[status] || STATUS.pending
  const isLast = phase === 4
  const canOpen = visible && status !== 'pending' && status !== 'skipped'

  return (
    <div style={{ display: 'flex', gap: '12px', opacity: visible ? 1 : 0.35, transition: `opacity 0.3s ease ${index * 0.08}s` }}>

      {/* Dot + line */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', flexShrink: 0 }}>
        <div style={{
          width: '28px', height: '28px', borderRadius: '50%',
          background: visible ? cfg.dot : 'var(--border)',
          border: `1.5px solid ${visible ? cfg.color : 'var(--border-dark)'}`,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '11px', fontWeight: 700, color: cfg.color,
          fontFamily: 'var(--font-body)',
          transition: `all 0.3s ease ${index * 0.08}s`,
          flexShrink: 0,
          cursor: canOpen ? 'pointer' : 'default',
        }} onClick={() => canOpen && setOpen(o => !o)}>{phase}</div>
        {!isLast && (
          <div style={{
            width: '1.5px', flex: 1, minHeight: '16px',
            background: visible ? 'var(--border-dark)' : 'var(--border)',
            margin: '4px 0',
          }} />
        )}
      </div>

      {/* Content */}
      <div style={{ paddingBottom: isLast ? 0 : '8px', flex: 1, minWidth: 0 }}>

        {/* Header row — clickable */}
        <div
          onClick={() => canOpen && setOpen(o => !o)}
          style={{
            display: 'flex', alignItems: 'center', gap: '6px',
            cursor: canOpen ? 'pointer' : 'default',
            marginBottom: open ? '8px' : '0',
            userSelect: 'none',
          }}
        >
          <span style={{
            fontFamily: 'var(--font-body)', fontSize: '13px',
            fontWeight: 600, color: 'var(--text)', flex: 1,
          }}>{name}</span>

          {visible && status !== 'pending' && (
            <span style={{
              fontSize: '10px', fontWeight: 600, color: cfg.color,
              background: cfg.dot, padding: '2px 7px',
              borderRadius: '100px', fontFamily: 'var(--font-body)',
              flexShrink: 0,
            }}>{cfg.label}</span>
          )}

          {canOpen && (
            <span style={{
              fontSize: '10px', color: 'var(--text-light)',
              transition: 'transform 0.2s',
              transform: open ? 'rotate(180deg)' : 'rotate(0deg)',
              display: 'inline-block', flexShrink: 0,
            }}>▾</span>
          )}
        </div>

        {/* Expandable detail */}
        {open && canOpen && result && (
          <div style={{
            background: 'var(--bg)',
            border: '1px solid var(--border)',
            borderRadius: '8px',
            padding: '12px',
            animation: 'slideDown 0.2s ease',
          }}>
            <PhaseDetail phase={phase} result={result} />
          </div>
        )}

        {visible && status === 'skipped' && (
          <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-body)', marginTop: '2px' }}>
            Las reglas resolvieron el enunciado
          </p>
        )}
      </div>

      <style>{`
        @keyframes slideDown {
          from { opacity: 0; transform: translateY(-6px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  )
}

function Row({ label, value }) {
  return (
    <div style={{
      display: 'flex', justifyContent: 'space-between', gap: '8px',
      padding: '4px 0',
      borderBottom: '1px solid var(--border)',
    }}>
      <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-body)', flexShrink: 0 }}>{label}</span>
      <span style={{ fontSize: '11px', color: 'var(--text)', fontFamily: 'var(--font-body)', textAlign: 'right', wordBreak: 'break-word' }}>{value}</span>
    </div>
  )
}

function PhaseDetail({ phase, result }) {
  if (phase === 1) return (
    <div>
      <Row label="Tokens" value={result.token_count} />
      <Row label="Negación" value={result.has_negation ? '⚠ Sí' : 'No'} />
      {result.numbers_found?.length > 0 && <Row label="Números" value={result.numbers_found.join(', ')} />}
      <div style={{ marginTop: '8px', display: 'flex', flexWrap: 'wrap', gap: '3px' }}>
        {result.tokens?.map((t, i) => (
          <span key={i} style={{
            padding: '2px 7px', borderRadius: '4px', fontSize: '10px',
            fontFamily: 'var(--font-body)',
            background: tokenBg(t.type), color: tokenColor(t.type),
            border: `1px solid ${tokenColor(t.type)}30`,
          }}>{t.value}</span>
        ))}
      </div>
    </div>
  )

  if (phase === 2) return (
    <div>
      <Row label="Tipo" value={result.structure_type} />
      {result.subject && <Row label="Sujeto" value={result.subject} />}
      {result.verb    && <Row label="Verbo"  value={result.verb} />}
      {result.warnings?.map((w, i) => (
        <p key={i} style={{ fontSize: '11px', color: 'var(--unknown-color)', marginTop: '6px', fontFamily: 'var(--font-body)' }}>⚠ {w}</p>
      ))}
    </div>
  )

  if (phase === 3) return (
    <div>
      <Row label="Veredicto" value={result.verdict} />
      <Row label="Método"    value={result.method} />
      <Row label="Confianza" value={`${(result.confidence * 100).toFixed(0)}%`} />
      {result.needs_ai && (
        <p style={{ fontSize: '11px', color: 'var(--ai-color)', marginTop: '6px', fontFamily: 'var(--font-body)' }}>
          → Pasando a Fase 4 (IA)
        </p>
      )}
    </div>
  )

  if (phase === 4) {
    if (result.skipped) return (
      <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-body)' }}>
        No fue necesaria — las reglas resolvieron el enunciado.
      </p>
    )
    return (
      <div>
        <Row label="Modelo"    value="Groq · Llama 3.1" />
        <Row label="Confianza" value={`${(result.confidence * 100).toFixed(0)}%`} />
        {result.explanation && (
          <p style={{
            fontSize: '11px', color: 'var(--text-muted)',
            fontStyle: 'italic', marginTop: '8px',
            fontFamily: 'var(--font-body)', lineHeight: 1.5,
          }}>"{result.explanation}"</p>
        )}
      </div>
    )
  }

  return null
}

function tokenColor(type) {
  const map = {
    NUMERO: '#D97706', NEGACION: '#DC2626', VERBO: '#2563EB',
    NOMBRE_PROPIO: '#16A34A', STOPWORD: '#94A3B8',
    CANTIDAD: '#7C3AED', SUSTANTIVO_O_ADJETIVO: '#475569',
  }
  return map[type] || '#94A3B8'
}

function tokenBg(type) {
  const map = {
    NUMERO: '#FFFBEB', NEGACION: '#FFF5F5', VERBO: '#EFF6FF',
    NOMBRE_PROPIO: '#F0FBF4', STOPWORD: '#F8FAFC',
    CANTIDAD: '#F5F3FF', SUSTANTIVO_O_ADJETIVO: '#F8FAFC',
  }
  return map[type] || '#F8FAFC'
}
