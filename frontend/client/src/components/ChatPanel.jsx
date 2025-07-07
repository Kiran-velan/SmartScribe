import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import ChatInput from "./ChatInput";
import WelcomePage from "../pages/WelcomePage"; 

const ChatPanel = () => {
  const { sessionId } = useParams();
  const [messages, setMessages] = useState([]);
  const [title, setTitle] = useState("");
  const [transcripts, setTranscripts] = useState([]);
  const [showTranscript, setShowTranscript] = useState(false);

  useEffect(() => {
    // Fetch transcripts for the session
    const fetchTranscripts = async () => {
      try {
        const res = await fetch(`http://localhost:8000/transcripts/by-session?session_id=${sessionId}`);
        const data = await res.json();
        if (res.ok) setTranscripts(data.transcripts);
        else console.error("Transcript fetch error:", data.error);
      } catch (err) {
        console.error("Transcript fetch error:", err);
      }
    };

    const fetchMessages = async () => {
      try {
        const res = await fetch(`http://localhost:8000/messages?session_id=${sessionId}`);
        const data = await res.json();
        console.log("Fetched messages:", data.messages);
        if (res.ok) setMessages(data.messages);
        else console.error(data.error);
      } catch (err) {
        console.error("Message fetch error:", err);
      }
    };

    const fetchSession = async () => {
      try {
        const res = await fetch(`http://localhost:8000/sessions/${sessionId}`);
        const data = await res.json();
        if (res.ok) setTitle(data.session?.title || "");
      } catch (err) {
        console.error("Failed to fetch session title", err);
      }
    };

    if (sessionId) {
      fetchSession();
      fetchMessages();
      fetchTranscripts();
    }
  }, [sessionId]);

  // Show Welcome if no sessionId
  if (!sessionId) {
    return (
      <div className="flex-1 flex flex-col justify-center items-center p-6">
        <WelcomePage />
      </div>
    );
  }

  const handleNewMessage = (msg) => {
    setMessages((prev) => [...prev, msg]);
  };

  const handleRename = async () => {
    const newTitle = window.prompt("Enter new title:", title);
    if (!newTitle || newTitle === title) return;

    try {
      const res = await fetch(`http://localhost:8000/sessions/${sessionId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle }),
      });

      const data = await res.json();
      if (res.ok) setTitle(newTitle);
      else console.error("Rename failed:", data.error);
    } catch (err) {
      console.error("Error renaming session:", err);
    }
  };

  const refreshTranscripts = async () => {
    const res = await fetch(`http://localhost:8000/transcripts/by-session?session_id=${sessionId}`);
    const data = await res.json();
    if (res.ok) setTranscripts(data.transcripts);
    else console.error("Transcript fetch error:", data.error);
  };

  return (
    <div className="flex-1 flex flex-col">
      <div className="px-4 py-2 border-b bg-gray-50 flex justify-between items-center">
        <h2 className="text-lg font-semibold">{title || "Untitled Session"}</h2>
        <div className="flex gap-4">
          <button
            onClick={() => setShowTranscript(!showTranscript)}
            className="text-sm text-purple-600 hover:underline"
          >
            {showTranscript ? "Hide Transcript" : "Show Transcript"}
          </button>
          <button
            onClick={handleRename}
            className="text-sm text-blue-600 hover:underline"
          >
            Rename
          </button>
        </div>
      </div>
      {showTranscript && transcripts.length > 0 && (
        <div className="bg-yellow-50 p-4 overflow-y-auto max-h-48">
          {transcripts.map((t) => (
            <div key={t.$id} className="mb-4">
              <p className="font-bold">{t.title}</p>
              <p className="text-sm text-gray-800 whitespace-pre-wrap">{t.original_text}</p>
            </div>
          ))}
        </div>
      )}

      <div className="flex-1 p-6 overflow-y-auto">
        {messages.length === 0 && (
          <div className="text-gray-500 text-center mt-4">No messages yet.</div>
        )}
        {messages.map((msg) =>
          msg && msg.sender && msg.text ? (
            <div key={msg.$id} className={`mb-4 ${msg.sender === "user" ? "text-right" : "text-left"}`}>
              <div className={`inline-block px-4 py-3 rounded-lg max-w-md ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800" }`}>
                <p>{msg.text}</p>
              </div>
            </div>
          ) : null
        )}
      </div>
      <ChatInput sessionId={sessionId} onNewMessage={handleNewMessage} onTranscriptUpload={refreshTranscripts} />
    </div>
  );
};

export default ChatPanel;
// This component fetches messages for a specific session and displays them.
// It also includes the ChatInput component for sending new messages.
// The messages are displayed in a scrollable area, with user messages aligned to the right and
// assistant messages aligned to the left. Also the messages are send with user and ai labels.