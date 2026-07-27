import { useState } from "react";
import "../css/ChatInput.css";

function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState("");

  function handleSend() {
    if (!message.trim() || loading) return;
    onSend(message);
    setMessage("");
  }

  return (
    <div className="chat-input-container">
      <div className="chat-input-wrapper">
        <textarea
          className="chat-textarea"
          placeholder="Describe your IT issue..."
          value={message}
          disabled={loading}
          rows={1}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />
        <button 
          className="send-button" 
          onClick={handleSend} 
          disabled={loading || !message.trim()}
          title="Send message"
        >
          {loading ? (
            <span className="spinner"></span>
          ) : (
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
            </svg>
          )}
        </button>
      </div>
      <div className="input-hint">Press Enter to send, Shift + Enter for new line</div>
    </div>
  );
}

export default ChatInput;
