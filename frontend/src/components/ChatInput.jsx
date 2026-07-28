import { useState, useRef } from "react";
import { Mic, Send, Loader2 } from "lucide-react";
import "../css/ChatInput.css";

function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState("");
  const [isListening, setIsListening] = useState(false);

  const recognitionRef = useRef(null);

  function handleSend() {
    if (!message.trim() || loading) return;

    onSend(message);
    setMessage("");
  }

  function startListening() {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition is not supported in this browser.");
      return;
    }

    // Stop if already listening
    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = false;

    recognitionRef.current = recognition;

    setIsListening(true);

    recognition.onresult = (event) => {
      let transcript = "";

      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }

      setMessage(transcript);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = () => {
      setIsListening(false);
    };

    recognition.start();
  }

  return (
    <div className="chat-input-container">

      <div className="chat-input-wrapper">

        <textarea
          className="chat-textarea"
          placeholder={
            isListening
              ? "Listening..."
              : "Describe your IT issue..."
          }
          value={message}
          disabled={loading}
          rows={1}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <button
          className={`mic-button ${isListening ? "active" : ""}`}
          onClick={startListening}
          disabled={loading}
          title="Voice Input"
        >
          <Mic size={20} />
        </button>

        <button
          className="send-button"
          onClick={handleSend}
          disabled={loading || !message.trim()}
          title="Send Message"
        >
          {loading ? (
            <Loader2 className="spinner-icon" size={20} />
          ) : (
            <Send size={20} />
          )}
        </button>

      </div>

      <div className="input-hint">
        {isListening
          ? "🎤 Listening... Speak now"
          : "Press Enter to send, Shift +Enter for new line"}
      </div>

    </div>
  );
}

export default ChatInput;