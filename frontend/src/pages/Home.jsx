import { useState } from "react";
import ChatInput from "../components/ChatInput";
import ChatWindow from "../components/ChatWindow";
import { sendMessage } from "../services/api";
 
function Home() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
 
  async function handleSend(text) {
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text,
        timestamp: timeStr
      }
    ]);
 
    setLoading(true);
 
    try {
      const response = await sendMessage(text);
      const resTimeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
 
      setMessages((prev) => [
        ...prev,
        {
          type: "system",
          text: `Executing workflow: ${response.workflow}`,
          workflow: response.workflow,
          logs: response.logs,
          timestamp: resTimeStr
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          type: "system",
          text: "An error occurred while contacting the support backend.",
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setLoading(false);
    }
  }
 
  return (
<div className="app-layout">
<header className="app-header">
<div className="header-brand">
<span className="brand-logo">🛡️</span>
<div>
<h1 className="brand-title">AI IT Support Agent</h1>
<p className="brand-subtitle">Automated Support for Teams, Outlook & System Issues</p>
</div>
</div>
<div className="header-status">
<span className="status-indicator online"></span>
<span className="status-text">System Ready</span>
</div>
</header>
 
      <main className="chat-container">
<ChatWindow messages={messages} loading={loading} />
<ChatInput onSend={handleSend} loading={loading} />
</main>
</div>
  );
}
 
export default Home;