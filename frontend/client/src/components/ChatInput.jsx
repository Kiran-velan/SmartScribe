import React, { useState, useRef } from "react";
import { useAuth } from "../context/AuthContext";

const ChatInput = ({ sessionId, onNewMessage, onTranscriptUpload }) => {
  const { user } = useAuth();
  const [input, setInput] = useState("");
  const fileInputRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const res = await fetch("http://localhost:8000/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        sender: "user",
        text: input
      })
    });

    const data = await res.json();
    if (res.ok) {
      onNewMessage(data.message_doc);
      setInput("");
    } else {
      console.error(data.error);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !user) return;

    const title = window.prompt("Enter a title for this transcript:");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("session_id", sessionId);
    formData.append("user_id", user.$id);
    formData.append("title", title || file.name); // fallback

    setIsUploading(true);
    const res = await fetch("http://localhost:8000/transcripts", {
      method: "POST",
      body: formData,
    });
    setIsUploading(false);

    const data = await res.json();
    if (res.ok) {
      if (onTranscriptUpload) onTranscriptUpload(); // 🔁 Refresh transcript list
    } else {
      console.error("Transcript upload failed:", data.error);
    }
  };

  const handleYouTubeLink = async () => {
    const url = window.prompt("Paste a YouTube link:");
    if (!url || !user) return;

    const title = window.prompt("Enter a title for this YouTube transcript:");
    setIsUploading(true);
    const res = await fetch("http://localhost:8000/transcripts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        user_id: user.$id,
        title: title || url,
        youtube_url: url, // your backend will detect this and process accordingly
      }),
    });
    setIsUploading(false);

    const data = await res.json();
    if (res.ok) {
      if (onTranscriptUpload) onTranscriptUpload(); // 🔁 Refresh transcript list
    } else {
      console.error("YouTube upload failed:", data.error);
    }
  };

  return (
    <div className="flex flex-col gap-2 p-4 border-t">
      <div className="flex gap-2">
        <input
          className="flex-1 border p-2 rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button
          onClick={handleSend}
          className="bg-blue-500 text-white px-4 rounded"
        >
          Send
        </button>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => fileInputRef.current.click()}
          className="bg-gray-700 text-white px-3 py-1 rounded"
        >
          Upload File
        </button>
        <input
          type="file"
          accept="audio/*,video/*"
          ref={fileInputRef}
          className="hidden"
          onChange={handleFileUpload}
        />

        <button
          onClick={handleYouTubeLink}
          className="bg-red-600 text-white px-3 py-1 rounded"
        >
          Add YouTube Link
        </button>
        {isUploading && (
          <div className="text-sm text-gray-600 italic mt-2">
            Transcribing... This may take a moment.
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatInput;

// This component renders an input field and a send button.
// It handles sending messages to the backend and updating the chat.
// It takes `sessionId` and `onNewMessage` as props to manage the chat state and session context.