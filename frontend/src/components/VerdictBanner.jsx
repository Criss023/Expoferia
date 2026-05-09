const CONFIGS = {
  VERDADERO: {
    bg: 'var(--true-bg)', color: 'var(--true-color)',
    border: 'var(--true-border)', soft: 'var(--true-soft)',
    emoji: '✓', label: 'Verdadero',
    desc: 'El enunciado es factualmente correcto'
  },
  FALSO: {
    bg: 'var(--false-bg)', color: 'var(--false-color)',
    border: 'var(--false-border)', soft: 'var(--false-soft)',
    emoji: '✗', label: 'Falso',
    desc: 'El enunciado contiene información incorrecta'
  },
  INDETERMINADO: {
    bg: 'var(--unknown-bg)', color: 'var(--unknown-color)',
    border: 'var(--unknown-border)', soft: 'var(--unknown-soft)',
    emoji: '?', label: 'Indeterminado',
    desc: 'No se pudo verificar con certeza'
  },
  NO_VERIFICABLE: {
    bg: 'var(--surface)', color: 'var(--text-muted)',
    border: 'var(--border)', soft: 'var(--border)',
    emoji: '—', label: 'No verificable',
    desc: 'El enunciado no puede verificarse objetivamente'
  },
}

const METHOD_LABELS = {
  REGLA_MATEMATICA: 'Regla matemática',
  REGLA_BASE_CONOCIMIENTO: 'Base de conocimiento',
  IA_GROQ: 'Determinado por IA',
  IA_GEMINI: 'Determinado por IA',
  IA_CLAUDE: 'Determinado por IA',
  IA_ERROR: 'Error de conexión IA',
  SIN_REGLA: 'Sin regla aplicable',
}

export default function VerdictBanner({ verdict, confidence, method, explanation, processingTime, sentence }) {
  const cfg = CONFIGS[verdict] || CONFIGS.NO_VERIFICABLE
  const isAI = method?.startsWith('IA_') && method !== 'IA_ERROR'

  return (
    <div style={{
      background: cfg.bg,
      border: `1.5px solid ${cfg.border}`,
      borderRadius: 'var(--radius)',
      padding: '40px',
      textAlign: 'center',
      animation: 'fadeUp 0.45s cubic-bezier(0.16, 1, 0.3, 1)',
      boxShadow: 'var(--shadow-md)',
    }}>
      {/* Sentence */}
      <p style={{
        fontFamily: 'var(--font-body)',
        fontSize: '13px',
        color: 'var(--text-muted)',
        marginBottom: '28px',
        padding: '10px 18px',
        background: 'rgba(255,255,255,0.7)',
        borderRadius: '100px',
        display: 'inline-block',
        border: '1px solid var(--border)',
        fontStyle: 'italic',
        letterSpacing: '0.01em',
      }}>"{sentence}"</p>

      {/* Big icon */}
      <div style={{
        width: '80px', height: '80px',
        borderRadius: '50%',
        background: cfg.soft,
        border: `2px solid ${cfg.border}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        margin: '0 auto 20px',
        fontSize: '32px',
        fontWeight: 700,
        color: cfg.color,
        fontFamily: 'var(--font-display)',
        animation: 'popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) 0.1s both',
      }}>{cfg.emoji}</div>

      {/* Label */}
      <h2 style={{
        fontFamily: 'var(--font-display)',
        fontSize: '48px',
        fontWeight: 700,
        color: cfg.color,
        letterSpacing: '-1px',
        lineHeight: 1,
        marginBottom: '8px',
      }}>{cfg.label}</h2>

      <p style={{
        fontFamily: 'var(--font-body)',
        fontSize: '14px',
        color: 'var(--text-muted)',
        marginBottom: '24px',
        fontWeight: 400,
      }}>{cfg.desc}</p>

      {/* Explanation */}
      {explanation && !explanation.startsWith('HTTP') && (
        <div style={{
          background: 'rgba(255,255,255,0.8)',
          border: `1px solid ${cfg.border}`,
          borderLeft: `3px solid ${cfg.color}`,
          borderRadius: 'var(--radius-sm)',
          padding: '14px 18px',
          maxWidth: '480px',
          margin: '0 auto 24px',
          textAlign: 'left',
        }}>
          <p style={{
            fontFamily: 'var(--font-body)',
            fontSize: '14px',
            color: 'var(--text)',
            lineHeight: 1.65,
            fontWeight: 400,
          }}>{explanation}</p>
        </div>
      )}

      {/* Meta chips */}
      <div style={{ display: 'flex', justifyContent: 'center', gap: '8px', flexWrap: 'wrap' }}>
        <Chip label={METHOD_LABELS[method] || method} color={cfg.color} border={cfg.border} />
        <Chip label={`${(confidence * 100).toFixed(0)}% confianza`} color={cfg.color} border={cfg.border} />
        <Chip label={`${processingTime}ms`} color={cfg.color} border={cfg.border} />
        {isAI && <Chip label="🤖 IA" color="var(--ai-color)" border="var(--ai-border)" bg="var(--ai-bg)" />}
      </div>

      <style>{`
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(16px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes popIn {
          from { transform: scale(0.5); opacity: 0; }
          to   { transform: scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  )
}

function Chip({ label, color, border, bg }) {
  return (
    <span style={{
      padding: '5px 12px',
      borderRadius: '100px',
      fontSize: '12px',
      fontFamily: 'var(--font-body)',
      fontWeight: 500,
      color,
      background: bg || 'rgba(255,255,255,0.8)',
      border: `1px solid ${border}`,
    }}>{label}</span>
  )
}
