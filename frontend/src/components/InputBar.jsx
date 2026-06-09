import { useState, useRef } from 'react'
import './InputBar.css'

export default function InputBar({
  onSend,
  onStop,
  loading,
  placeholder = 'Mevzuat hakkında bir soru sorun… (Enter ile gönder)',
  hint = 'Shift+Enter ile yeni satır ekleyin',
}) {
  const [text, setText] = useState('')
  const textareaRef = useRef(null)

  const handleSubmit = () => {
    const trimmed = text.trim()
    if (!trimmed) return
    onSend(trimmed)
    setText('')
    textareaRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleInput = (e) => {
    setText(e.target.value)
    const el = textareaRef.current
    if (el) {
      el.style.height = 'auto'
      el.style.height = Math.min(el.scrollHeight, 150) + 'px'
    }
  }

  return (
    <div className="input-bar">
      <div className="input-wrapper">
        <textarea
          ref={textareaRef}
          className="input-field"
          rows={1}
          value={text}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={loading}
        />
        {loading ? (
          <button className="btn btn-stop" onClick={onStop} title="Durdur">
            ⏹
          </button>
        ) : (
          <button
            className="btn btn-send"
            onClick={handleSubmit}
            disabled={!text.trim()}
            title="Gönder"
          >
            ➤
          </button>
        )}
      </div>
      <p className="hint">{hint}</p>
    </div>
  )
}
