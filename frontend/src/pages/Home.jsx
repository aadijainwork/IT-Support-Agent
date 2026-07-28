import { useState } from "react";

import Sidebar from "../components/Sidebar";
import Header from "../components/Header";
import ChatArea from "../components/ChatArea";
import ChatInput from "../components/ChatInput";

import { sendMessage } from "../services/api";

import "../css/Home.css";

function Home() {

  const [loading, setLoading] = useState(false);

  const [chats, setChats] = useState([
    {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    },
  ]);

  const [activeChatId, setActiveChatId] = useState(chats[0].id);

  const activeChat =
    chats.find((chat) => chat.id === activeChatId) || chats[0];

  function updateActiveChat(newMessages) {
    setChats((prevChats) =>
      prevChats.map((chat) =>
        chat.id === activeChatId
          ? {
              ...chat,
              messages: newMessages,
            }
          : chat
      )
    );
  }

  function handleNewChat() {
    const newChat = {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    };

    setChats((prev) => [...prev, newChat]);
    setActiveChatId(newChat.id);
  }

  function handleSelectChat(id) {
    setActiveChatId(id);
  }

  async function handleSend(text) {

    const currentTime = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    const userMessage = {
      type: "user",
      text,
      timestamp: currentTime,
    };

    let updatedMessages = [
      ...activeChat.messages,
      userMessage,
    ];

    setChats((prevChats) =>
      prevChats.map((chat) => {
        if (chat.id !== activeChatId) return chat;

        return {
          ...chat,
          title:
            chat.title === "New Chat"
              ? text.length > 30
                ? text.substring(0, 30) + "..."
                : text
              : chat.title,
          messages: updatedMessages,
        };
      })
    );

    setLoading(true);

    try {

      const response = await sendMessage(text);

      const responseTime = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      updatedMessages = [
        ...updatedMessages,
        {
          type: "system",
          workflow: response.workflow,
          logs: response.logs,
          text: `Executing workflow: ${response.workflow}`,
          timestamp: responseTime,
        },
      ];

      updateActiveChat(updatedMessages);

    } catch (error) {

      updatedMessages = [
        ...updatedMessages,
        {
          type: "system",
          text: "Unable to connect to the backend.",
          timestamp: currentTime,
        },
      ];

      updateActiveChat(updatedMessages);

    } finally {

      setLoading(false);

    }

  }

      return (
    <div className="home">

      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
      />

      <div className="main-content">

        <Header />

        <main className="content-area">

          <ChatArea
            messages={activeChat.messages}
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
