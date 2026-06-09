import { useEffect, useRef } from 'react'
import Message from './Message'
import { formatDateLabel, getDayKey } from '../utils/date'
import './ChatWindow.css'

export default function ChatWindow({ messages }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const items = []
  let lastDayKey = null

  for (const msg of messages) {
    const dayKey = getDayKey(msg.timestamp)
    if (dayKey !== lastDayKey) {
      items.push({ type: 'separator', key: `sep-${dayKey}`, label: formatDateLabel(msg.timestamp) })
      lastDayKey = dayKey
    }
    items.push({ type: 'message', key: msg.id, msg })
  }

  return (
    <div className="chat-window">
      {items.map((item) =>
        item.type === 'separator' ? (
          <div key={item.key} className="date-separator">
            <span>{item.label}</span>
          </div>
        ) : (
          <Message key={item.key} message={item.msg} />
        )
      )}
      <div ref={bottomRef} />
    </div>
  )
}
