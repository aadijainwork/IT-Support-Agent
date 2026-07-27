import { useState } from "react";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import ChatArea from "../components/ChatArea";
import ChatInput from "../components/ChatInput";

import { sendMessage } from "../services/api";

import "../css/Home.css";

function Home() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(text) {
    const currentTime = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    // Add user message
    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text,
        timestamp: currentTime,
      },
    ]);

    setLoading(true);

    try {
      const response = await sendMessage(text);

      const responseTime = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      setMessages((prev) => [
        ...prev,
        {
          type: "system",
          workflow: response.workflow,
          logs: response.logs,
          text: `Executing workflow: ${response.workflow}`,
          timestamp: responseTime,
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          type: "system",
          text: "Unable to connect to the backend.",
          timestamp: currentTime,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="home">
      <Sidebar />

      <div className="main-content">
        <Header />

        <main className="content-area">
          <ChatArea
            messages={messages}
            loading={loading}
          />

          <ChatInput
            onSend={handleSend}
            loading={loading}
          />
        </main>
      </div>
    </div>
  );
}

export default Home;