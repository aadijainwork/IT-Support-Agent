import WelcomeScreen from "./WelcomeScreen";
import ChatWindow from "./ChatWindow";
import "../css/ChatArea.css";

function ChatArea({
  messages = [],
  loading,
}) {
  return (
    <div className="chat-area">
      {messages.length === 0 ? (
        <WelcomeScreen />
      ) : (
        <ChatWindow
          messages={messages}
          loading={loading}
        />
      )}
    </div>
  );
}

export default ChatArea;