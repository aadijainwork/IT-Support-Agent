import "../css/WelcomeScreen.css";
import { Bot } from "lucide-react";

function WelcomeScreen() {
  return (
    <div className="welcome-screen">

      <div className="welcome-icon">
        <Bot size={55} />
      </div>

      <h1>Welcome to AI IT Support Assistant</h1>

      <p>
        Resolve Microsoft Teams, Outlook and Windows issues
        using automated troubleshooting workflows.
      </p>

      <div className="quick-prompts">

        <button>Teams not launching</button>

        <button>Outlook not syncing</button>

        <button>Teams update issue</button>

        <button>Computer running slow</button>

      </div>

    </div>
  );
}

export default WelcomeScreen;