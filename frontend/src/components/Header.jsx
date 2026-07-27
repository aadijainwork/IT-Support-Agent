import "../css/Header.css";
import { Bell, UserCircle } from "lucide-react";

function Header() {
  return (
    <header className="header">

      <div className="header-left">
        <h1>AI IT Support Assistant</h1>
        <p>Automated troubleshooting for Microsoft Teams and Outlook</p>
      </div>

      <div className="header-right">

        <button className="notification-btn">
          <Bell size={20} />
        </button>

        <div className="profile">
          <UserCircle size={36} />
          <div>
            <h4>Varad</h4>
            <span>IT Support User</span>
          </div>
        </div>

      </div>

    </header>
  );
}

export default Header;