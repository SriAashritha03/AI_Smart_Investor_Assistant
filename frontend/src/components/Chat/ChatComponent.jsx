import React, { useState, useRef, useEffect } from 'react'
import './ChatComponent.css'

function ChatComponent({ onSendMessage }) {
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('chat_history')
    return saved ? JSON.parse(saved) : [
      {
        id: 1,
        role: 'bot',
        text: 'Hello! I\'m your Financial AI Assistant. How can I help you analyze the markets today?'
      }
    ]
  })
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    localStorage.setItem('chat_history', JSON.stringify(messages))
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage = {
      id: Date.now(),
      role: 'user',
      text: inputValue
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      let response = ''
      if (onSendMessage) {
        response = await onSendMessage(inputValue)
      } else {
        const apiResponse = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: inputValue })
        })
        if (!apiResponse.ok) throw new Error(`HTTP ${apiResponse.status}`)
        const data = await apiResponse.json()
        response = data.reply
      }
      
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'bot',
        text: response || 'I couldn\'t process that request. Please try again.'
      }])
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'bot',
        text: `Technical Error: ${error.message}`
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const clearChatHistory = () => {
    if (window.confirm('Clear all conversation history?')) {
      setMessages([{
        id: 1,
        role: 'bot',
        text: 'System cleared. How can I help you analyze the markets?'
      }])
      localStorage.removeItem('chat_history')
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <span className="material-symbols-outlined chat-header-icon" style={{ fontSize: '24px', color: 'var(--primary)' }}>auto_awesome</span>
        <h3 className="chat-title">Intelligence Interface</h3>
        <button onClick={clearChatHistory} className="clear-chat-btn" title="Clear History">
          <span className="material-symbols-outlined" style={{ fontSize: '20px' }}>delete_sweep</span>
        </button>
      </div>

      <div className="chat-messages">
        <div className="messages-container">
          {messages.length === 1 && messages[0].role === 'bot' && (
            <div className="system-greeting">
              <div className="greeting-icon">
                <span className="material-symbols-outlined">auto_awesome</span>
              </div>
              <h2 className="greeting-title">Intelligence Interface</h2>
              <p className="greeting-subtitle">System calibrated for high-frequency analysis and predictive modeling. How can I assist your portfolio today?</p>
            </div>
          )}
          
          {messages.map((msg, idx) => {
            const timestamp = new Date().toLocaleTimeString('en-US', { 
              hour: '2-digit', 
              minute: '2-digit',
              hour12: true 
            })
            return (
              <div key={msg.id} className={`chat-message ${msg.role === 'user' ? 'user-message' : 'bot-message'}`}>
                {msg.role === 'bot' && (
                  <div className="ai-avatar">
                    <span className="material-symbols-outlined">terminal</span>
                  </div>
                )}
                <div className={`message-wrapper ${msg.role}`}>
                  <div className={`message-bubble ${msg.role}`}>
                    <div className="message-text">
                      {msg.text.split('\n').map((line, idx) => (
                        <div key={idx}>{line}</div>
                      ))}
                    </div>
                    
                    {/* Insight Card - Only for bot messages */}
                    
                  </div>
                  
                  {/* Message Actions (Hover) */}
                  {msg.role === 'bot' && (
                    <div className="message-actions">
                      <button className="action-button" title="Copy message">
                        <span className="material-symbols-outlined">content_copy</span>
                      </button>
                      <button className="action-button" title="Like">
                        <span className="material-symbols-outlined">thumb_up</span>
                      </button>
                      <button className="action-button" title="Dislike">
                        <span className="material-symbols-outlined">thumb_down</span>
                      </button>
                    </div>
                  )}
                  
                  <span className="message-timestamp">
                    {timestamp} • {msg.role === 'user' ? 'User' : 'Smart Investor Intelligence'}
                  </span>
                </div>
              </div>
            )
          })}
        {isLoading && (
          <div className="chat-message bot-message">
            <div className="ai-avatar">
              <span className="material-symbols-outlined">terminal</span>
            </div>
            <div className="message-wrapper bot">
              <div className="message-bubble bot">
                <div className="typing-indicator">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <div className="input-wrapper">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Inquire about market trends, portfolio data, or strategy..."
            className="chat-input"
            disabled={isLoading}
          />
          <button className="voice-button" title="Voice input" disabled={isLoading}>
            <span className="material-symbols-outlined">mic</span>
            <span className="voice-label">Voice</span>
          </button>
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
          >
            <span className="material-symbols-outlined">
              {isLoading ? 'hourglass_bottom' : 'send'}
            </span>
          </button>
        </div>
        <div className="status-indicators">
          <div className="status-item">
            <span className="status-dot synchronized"></span>
            <span className="status-text">Node 04: Synchronized</span>
          </div>
          <div className="status-item">
            <span className="status-dot latency"></span>
            <span className="status-text">Latency: 14ms</span>
          </div>
        </div>
      </div>
    </div>
    </div>
  )
}
export default ChatComponent;
