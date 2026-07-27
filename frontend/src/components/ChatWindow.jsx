import { useEffect, useRef, useState } from "react";
import "../css/ChatWindow.css";

function ChatWindow({ messages, loading }) {
  const messagesEndRef = useRef(null);

  // Stores how many logs are currently visible for each message
  const [visibleLogs, setVisibleLogs] = useState({});

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading, visibleLogs]);

  // Animate logs one-by-one
  useEffect(() => {
    messages.forEach((msg, msgIndex) => {
      if (
        msg.type !== "system" ||
        !msg.logs ||
        visibleLogs[msgIndex] !== undefined
      ) {
        return;
      }

      let current = 0;

      setVisibleLogs((prev) => ({
        ...prev,
        [msgIndex]: 0,
      }));

      const interval = setInterval(() => {
        current++;

        setVisibleLogs((prev) => ({
          ...prev,
          [msgIndex]: current,
        }));

        if (current >= msg.logs.length) {
          clearInterval(interval);
        }
      }, 600);

      return () => clearInterval(interval);
    });
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.length === 0 ? (
        <div className="chat-empty">
          <div className="empty-icon">🤖</div>

          <h3>Welcome to AI IT Support Agent</h3>

          <p>
            Describe an issue with Microsoft Teams, Outlook, Network, or
            Hardware devices to start troubleshooting.
          </p>
        </div>
      ) : (
        messages.map((msg, idx) => (
          <div
            key={idx}
            className={`message-row ${msg.type}`}
          >
            <div className="avatar">
              {msg.type === "user" ? "👤" : "🤖"}
            </div>

            <div className="message-bubble">
              <div className="message-header">
                <span className="sender-name">
                  {msg.type === "user"
                    ? "You"
                    : "IT Support Agent"}
                </span>

                {msg.timestamp && (
                  <span className="timestamp">
                    {msg.timestamp}
                  </span>
                )}
              </div>

              <div className="message-text">
                {msg.text ||
                  (msg.type === "system"
                    ? "Workflow execution response:"
                    : "")}
              </div>

              {msg.workflow && (
                <div className="workflow-badge">
                  <span className="workflow-label">
                    Workflow:
                  </span>{" "}
                  {msg.workflow}
                </div>
              )}

              {msg.logs && (
                <div className="logs-container">
                  <div className="logs-title">
                    Execution Steps
                  </div>

                  <ul className="logs-list">
                    {msg.logs
                      .slice(
                        0,
                        visibleLogs[idx] || 0
                      )
                      .map((log, logIdx) => (
                        <li
                          key={logIdx}
                          className="log-item"
                        >
                          <span
                            style={{
                              color: "#22c55e",
                              fontWeight: "bold",
                              marginRight: "10px",
                            }}
                          >
                            ✓
                          </span>

                          {log}
                        </li>
                      ))}

                    {(visibleLogs[idx] || 0) <
                      msg.logs.length && (
                      <li className="log-item">
                        <span
                          style={{
                            color: "#2563eb",
                            fontWeight: "bold",
                            marginRight: "10px",
                          }}
                        >
                          ⏳
                        </span>

                        {msg.logs[
                          visibleLogs[idx] || 0
                        ]}
                      </li>
                    )}
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