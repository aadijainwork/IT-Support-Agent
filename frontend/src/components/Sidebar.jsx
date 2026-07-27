import "../css/Sidebar.css";
import {
  MessageSquare,
  Plus,
  History,
  Ticket,
  Shield
} from "lucide-react";

export default function Sidebar() {
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

        <button className="new-chat-btn">
          <Plus size={18} />
          New Chat
        </button>

      </div>

      <div className="sidebar-menu">

        <div className="menu-item active">
          <MessageSquare size={20} />
          <span>Chat</span>
        </div>

        <div className="menu-item">
          <History size={20} />
          <span>History</span>
        </div>

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