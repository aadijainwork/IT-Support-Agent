import { useEffect, useRef } from "react";

function ChatWindow({ messages, loading }) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="chat-empty">
          <div className="empty-icon">🤖</div>
          <h3>Welcome to AI IT Support Agent</h3>
          <p>Describe an issue with Microsoft Teams, Outlook, Network, or Hardware devices to start troubleshooting.</p>
        </div>
      ) : (
        messages.map((msg, idx) => (
          <div key={idx} className={`message-row ${msg.type}`}>
            <div className="avatar">
              {msg.type === "user" ? "👤" : "🤖"}
            </div>
            <div className="message-bubble">
              <div className="message-header">
                <span className="sender-name">{msg.type === "user" ? "You" : "IT Support Agent"}</span>
                {msg.timestamp && <span className="timestamp">{msg.timestamp}</span>}
              </div>
              <div className="message-text">{msg.text || (msg.type === "system" ? "Workflow execution response:" : "")}</div>
              
              {msg.workflow && (
                <div className="workflow-badge">
                  <span className="workflow-label">Workflow:</span> {msg.workflow}
                </div>
              )}

              {msg.logs && msg.logs.length > 0 && (
                <div className="logs-container">
                  <div className="logs-title">Execution Steps:</div>
                  <ul className="logs-list">
                    {msg.logs.map((log, logIdx) => (
                      <li key={logIdx} className="log-item">
                        <span className="log-dot"></span>
                        {log}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))
      )}

      {loading && (
        <div className="message-row system">
          <div className="avatar">🤖</div>
          <div className="message-bubble loading-bubble">
            <span className="dot"></span>
            <span className="dot"></span>
            <span className="dot"></span>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatWindow;
