import { useState, useRef } from "react";
import {
  Mic,
  Send,
  Loader2,
  X,
} from "lucide-react";
import "../css/ChatInput.css";

function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState("");
  const [isListening, setIsListening] = useState(false);

  const recognitionRef = useRef(null);
  const shouldContinueListening = useRef(false);

  function handleSend() {
    if (!message.trim() || loading) return;

    onSend(message);
    setMessage("");
  }

  function stopListening() {
    shouldContinueListening.current = false;

    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }

    setIsListening(false);
  }

  function startListening() {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert(
        "Speech Recognition is not supported in this browser."
      );
      return;
    }

    if (isListening) {
      stopListening();
      return;
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognitionRef.current = recognition;

    shouldContinueListening.current = true;
    setIsListening(true);

    recognition.onresult = (event) => {
      let transcript = "";

      for (let i = 0; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript + " ";
      }

      setMessage(transcript.trim());
    };

    recognition.onend = () => {

  console.log("================================");
  console.log("Speech Recognition Ended");
  console.log("shouldContinueListening:", shouldContinueListening.current);
  console.log("================================");

  if (shouldContinueListening.current) {

    try {
      console.log("Restarting recognition...");
      recognition.start();
      return;
    } catch (err) {
      console.error("Restart failed:", err);
    }
  }

  recognitionRef.current = null;
  setIsListening(false);
};

recognition.onerror = (event) => {

  console.log("================================");
  console.log("Speech Recognition Error");
  console.log("Error:", event.error);
  console.log("Message:", event.message || "No message");
  console.log("================================");

  // Ignore silence
  if (event.error === "no-speech") {
    return;
  }

  shouldContinueListening.current = false;
  recognitionRef.current = null;
  setIsListening(false);
};

    recognition.start();
  }

  return (
    <>
      {isListening && (
        <div className="voice-modal-overlay">
          <div className="voice-modal">
            <button
              className="voice-close-btn"
              onClick={stopListening}
            >
              <X size={20} />
            </button>

            <div className="voice-mic-wrapper">
              <div className="voice-mic-ring"></div>

              <div className="voice-mic-circle">
                <Mic size={40} />
              </div>
            </div>

            <h2>AI Agent is Listening</h2>

            <p>Speak your IT issue clearly...</p>

            <div className="voice-transcript">
              {message ? (
                message
              ) : (
                <span className="voice-placeholder">
                  Start speaking...
                </span>
              )}
            </div>

            <div className="voice-wave">
              {Array.from({ length: 25 }).map((_, i) => (
                <span
                  key={i}
                  style={{
                    animationDelay: `${i * 0.08}s`,
                  }}
                />
              ))}
            </div>

            <div className="voice-status">
              <div className="voice-status-dot"></div>
              Listening...
            </div>

            <small>
              Click the microphone again or press ✕ to stop
            </small>
          </div>
        </div>
      )}

      <div className="chat-input-container">
        <div className="chat-input-wrapper">
          <textarea
            className="chat-textarea"
            placeholder="Describe your IT issue..."
            value={message}
            disabled={loading}
            rows={1}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (
                e.key === "Enter" &&
                !e.shiftKey
              ) {
                e.preventDefault();
                handleSend();
              }
            }}
          />

          <button
            type="button"
            className={`mic-button ${
              isListening ? "active" : ""
            }`}
            onClick={startListening}
            disabled={loading}
          >
            <Mic size={20} />
          </button>

          <button
            type="button"
            className="send-button"
            onClick={handleSend}
            disabled={
              loading || !message.trim()
            }
          >
            {loading ? (
              <Loader2
                className="spinner-icon"
                size={20}
              />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>

        <div className="input-hint">
          Press <strong>Enter</strong> to send •{" "}
          <strong>Shift + Enter</strong> for a new line
        </div>
      </div>
    </>
  );
}

export default ChatInput;