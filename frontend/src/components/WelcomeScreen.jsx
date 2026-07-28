import "../css/WelcomeScreen.css";
import { Bot } from "lucide-react";

function WelcomeScreen() {
  return (
    <div className="welcome-screen">

      <div className="welcome-icon">
        <Bot size={55} strokeWidth={2.2} />
      </div>

      <h1>Welcome to AI IT Support Assistant</h1>

      <p>
        Resolve Microsoft Teams, Outlook, Windows and IT infrastructure
        issues using intelligent automated troubleshooting workflows.
      </p>

    </div>
  );
}

export default WelcomeScreen;