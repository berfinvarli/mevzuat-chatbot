import ReactMarkdown from 'react-markdown'
import { formatTime } from '../utils/date'
import './Message.css'

export default function Message({ message }) {
  const isUser = message.role === 'user'

  return (
    <div className={`message-row ${isUser ? 'user' : 'assistant'}`}>
      {!isUser && <div className="avatar assistant-avatar">⚖️</div>}
      <div className="bubble-group">
        <div className={`bubble ${isUser ? 'bubble-user' : 'bubble-assistant'}`}>
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown>{message.content || (message.streaming ? '' : '…')}</ReactMarkdown>
          )}
          {message.streaming && !message.content && (
            <span className="typing-indicator">
              <span /><span /><span />
            </span>
          )}
        </div>
        {!message.streaming && (
          <span className={`message-time ${isUser ? 'message-time--user' : ''}`}>
            {formatTime(message.timestamp)}
          </span>
        )}
      </div>
      {isUser && <div className="avatar user-avatar">👤</div>}
    </div>
  )
}
