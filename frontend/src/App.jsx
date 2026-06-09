import { useEffect } from 'react'
import { useChat } from './hooks/useChat'
import { useCmsValue } from './hooks/useCms'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'
import './App.css'

export default function App() {
  const title = useCmsValue('mevzuat.chatbot.title', 'Mevzuat Chatbot')
  const subtitle = useCmsValue('mevzuat.chatbot.subtitle', 'Türk Hukuku & Mevzuat Asistanı')
  const welcome = useCmsValue('mevzuat.chatbot.welcome_message')
  const placeholder = useCmsValue('mevzuat.chatbot.input_placeholder')
  const hint = useCmsValue('mevzuat.chatbot.input_hint')

  const { messages, loading, sendMessage, handleStop } = useChat(welcome)

  useEffect(() => {
    document.title = title
  }, [title])

  return (
    <div className="app">
      <header className="header">
        <span className="header-icon">⚖️</span>
        <div>
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
      </header>
      <ChatWindow messages={messages} />
      <InputBar
        onSend={sendMessage}
        onStop={handleStop}
        loading={loading}
        placeholder={placeholder}
        hint={hint}
      />
    </div>
  )
}
