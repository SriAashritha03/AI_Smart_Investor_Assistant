import React, { useState, useRef, useEffect } from 'react'
import './ChatComponent.css'

function ChatComponent({ onSendMessage }) {
  const [messages, setMessages] = useState(() => {
    // Load messages from localStorage on component mount
    const saved = localStorage.getItem('chat_history')
    return saved ? JSON.parse(saved) : [
      {
        id: 1,
        role: 'bot',
        text: 'Hello! I\'m your Financial Assistant. Ask me about stocks, portfolio analysis, market trends, or investment strategies. How can I help you today?'
      }
    ]
  })
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Save messages to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('chat_history', JSON.stringify(messages))
  }, [messages])

  // Auto-scroll to latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      role: 'user',
      text: inputValue
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      let response = ''
      
      // Use provided handler or call backend API
      if (onSendMessage) {
        response = await onSendMessage(inputValue)
      } else {
        // Call backend API
        const apiResponse = await fetch('http://localhost:8000/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: inputValue })
        })
        
        if (!apiResponse.ok) {
          const errorData = await apiResponse.json()
          throw new Error(errorData.detail || `HTTP ${apiResponse.status}`)
        }
        
        const data = await apiResponse.json()
        response = data.reply
      }
      
      if (!response) {
        throw new Error('No response received')
      }
      
      // Add bot response
      const botMessage = {
        id: messages.length + 2,
        role: 'bot',
        text: response
      }
      
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage = {
        id: messages.length + 2,
        role: 'bot',
        text: `❌ Error: ${error.message || 'Unable to process your request'}`
      }
      setMessages(prev => [...prev, errorMessage])
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
    if (window.confirm('Are you sure? This will clear all chat history.')) {
      setMessages([
        {
          id: 1,
          role: 'bot',
          text: 'Hello! I\'m your Financial Assistant. Ask me about stocks, portfolio analysis, market trends, or investment strategies. How can I help you today?'
        }
      ])
      localStorage.removeItem('chat_history')
    }
  }

  return (
    <div className="chat-container">
      {/* Chat Header */}
      <div className="chat-header">
        <h3 className="chat-title">💬 Financial Assistant</h3>
        <p className="chat-subtitle">Ask anything about stocks & portfolios</p>
        <button 
          onClick={clearChatHistory} 
          className="clear-chat-btn"
          title="Clear chat history"
        >
          🗑️
        </button>
      </div>

      {/* Messages Area */}
      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`chat-message ${message.role === 'user' ? 'user-message' : 'bot-message'}`}
          >
            <div className={`message-bubble ${message.role}`}>
              {message.role === 'bot' && <span className="message-avatar">🤖</span>}
              <div className="message-text">
                {/* Render message text with newlines preserved */}
                {message.text.split('\n').map((line, idx) => (
                  <div key={idx}>{line}</div>
                ))}
              </div>
              {message.role === 'user' && <span className="message-avatar">👤</span>}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="chat-message bot-message">
            <div className="message-bubble bot">
              <span className="message-avatar">🤖</span>
              <div className="message-text">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        <div className="input-wrapper">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about stocks, portfolios, or market trends..."
            className="chat-input"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
            title="Send message (Enter)"
          >
            {isLoading ? '⏳' : '📤'}
          </button>
        </div>
        <p className="chat-help-text">💡 Tip: Press Enter to send, Shift+Enter for new line</p>
      </div>
    </div>
  )
}

export default ChatComponent
