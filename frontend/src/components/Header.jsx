import "../css/Header.css";
import { Bell, Bot } from "lucide-react";

function Header() {
  return (
    <header className="header">

      <div className="header-left">
        <h1>AI IT Support Assistant</h1>
        <p>Automated troubleshooting for Microsoft Teams and Outlook</p>
      </div>

      <div className="header-right">

        <div className="agent-status">
          <span className="status-dot"></span>
          <Bot size={16} />
          <span>AI Agent Online</span>
        </div>

        <button className="notification-btn">
          <Bell size={20} />
        </button>

      </div>

    </header>
  );
}

export default Header;