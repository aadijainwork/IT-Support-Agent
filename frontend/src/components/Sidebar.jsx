import "../css/Sidebar.css";
import {
  Plus,
  Ticket,
  Shield,
  MessageSquare,
} from "lucide-react";

export default function Sidebar({
  chats = [],
  activeChatId,
  onNewChat,
  onSelectChat,
}) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">

        <div className="logo-section">
          <div className="logo-circle">
            <Shield size={26} />
          </div>

          <div>
            <h2>AI IT Support</h2>
            <p>Enterprise Assistant</p>
          </div>
        </div>

        <button
          className="new-chat-btn"
          onClick={onNewChat}
        >
          <Plus size={18} />
          New Chat
        </button>

      </div>

      <div className="sidebar-menu">

        <h4 className="history-title">History</h4>

        <div className="history-list">

          {chats.length === 0 ? (
            <div className="empty-history">
              No previous chats
            </div>
          ) : (
            chats.map((chat) => (
              <div
                key={chat.id}
                className={`history-item ${
                  activeChatId === chat.id ? "active" : ""
                }`}
                onClick={() => onSelectChat(chat.id)}
              >
                <MessageSquare size={18} />
                <span>
                  {chat.title || "New Chat"}
                </span>
              </div>
            ))
          )}

        </div>

        <div className="menu-divider"></div>

        <div className="menu-item">
          <Ticket size={20} />
          <span>My Tickets</span>
        </div>

      </div>

      <div className="sidebar-footer">
        <small>Version 1.0</small>
      </div>
    </aside>
  );
}