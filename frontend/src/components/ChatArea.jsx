import WelcomeScreen from "./WelcomeScreen";
import ChatWindow from "./ChatWindow";
import "../css/ChatArea.css";

function ChatArea({ messages, loading }) {
  if (messages.length === 0) {
    return (
      <div className="chat-area">
        <WelcomeScreen />
      </div>
    );
  }

  return (
    <div className="chat-area">
      <ChatWindow
        messages={messages}
        loading={loading}
      />
    </div>
  );
}

export default ChatArea;