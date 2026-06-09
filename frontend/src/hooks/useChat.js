import { useState, useRef, useCallback, useEffect } from 'react'
import { fetchHistory, streamChat } from '../api/chatApi'
import { WELCOME_MSG } from '../constants/messages'
import { getSessionId } from '../utils/session'
import { parseSSE } from '../utils/sse'

function buildMessage(role, content, extra = {}) {
  return { id: crypto.randomUUID(), role, content, timestamp: Date.now(), ...extra }
}

export function useChat(welcomeContent) {
  const [messages, setMessages] = useState(() => [
    buildMessage('assistant', welcomeContent ?? WELCOME_MSG.content, { id: 'welcome' }),
  ])
  const [loading, setLoading] = useState(false)
  const abortRef = useRef(null)

  useEffect(() => {
    if (!welcomeContent) return
    setMessages((prev) =>
      prev.map((m) => (m.id === 'welcome' ? { ...m, content: welcomeContent } : m))
    )
  }, [welcomeContent])

  useEffect(() => {
    getSessionId()
    fetchHistory()
      .then(({ messages: history }) => {
        if (!history?.length) return
        setMessages((prev) => {
          const welcome = prev.find((m) => m.id === 'welcome')
          return [welcome, ...history.map((m) => buildMessage(m.role, m.content, {
            timestamp: m.created_at ? new Date(m.created_at).getTime() : Date.now(),
          }))]
        })
      })
      .catch(() => {})
  }, [])

  function updateMessage(id, updater) {
    setMessages((prev) => prev.map((m) => (m.id === id ? updater(m) : m)))
  }

  function handleEvent(event, assistantId) {
    if (event.type === 'token') {
      updateMessage(assistantId, (m) => ({ ...m, content: m.content + event.content }))
    } else if (event.type === 'error') {
      updateMessage(assistantId, (m) => ({ ...m, content: `Hata: ${event.message}`, streaming: false }))
    }
  }

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim() || loading) return

      const userMsg = buildMessage('user', text)
      const assistantMsg = buildMessage('assistant', '', { streaming: true })

      setMessages((prev) => [...prev, userMsg, assistantMsg])
      setLoading(true)

      const history = [...messages, userMsg].map(({ role, content }) => ({ role, content }))
      const controller = new AbortController()
      abortRef.current = controller

      try {
        const response = await streamChat(history, controller.signal)
        for await (const event of parseSSE(response)) {
          handleEvent(event, assistantMsg.id)
        }
      } catch (err) {
        if (err.name !== 'AbortError') {
          updateMessage(assistantMsg.id, (m) => ({ ...m, content: `Hata: ${err.message}`, streaming: false }))
        }
      } finally {
        updateMessage(assistantMsg.id, (m) => ({ ...m, streaming: false }))
        setLoading(false)
      }
    },
    [messages, loading]
  )

  const handleStop = () => {
    abortRef.current?.abort()
    setLoading(false)
  }

  return { messages, loading, sendMessage, handleStop }
}
