import React, { useState, useRef } from "react";
import { useAuth } from "../context/AuthContext";

const ChatInput = ({ sessionId, onNewMessage, onTranscriptUpload }) => {
  const { user } = useAuth();
  const [input, setInput] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const fileInputRef = useRef(null);

  const handleSend = async () => {
    if (!input.trim() || isUploading || isThinking) return;

    setIsThinking(true);

    try {
      // 1. Store user message
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
        onNewMessage(data.message_doc);  // Show user message immediately
        setInput("");

        // 2. Trigger AI response from /talk endpoint
        const talkRes = await fetch("http://localhost:8000/talk", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: sessionId,
            prompt: input
          })
        });

        const talkData = await talkRes.json();
        // Use the response from /talk (already stored in messages too)
        if (talkRes.ok) {
          onNewMessage({
            session_id: sessionId,
            sender: "assistant",
            text: talkData.response,
            timestamp: new Date().toISOString()
          });
        } else {
          console.error("Talk failed:", talkData.detail || talkData.error);
        }
      } else {
        console.error("Message store failed:", data.error);
      }
    } catch (error) {
      console.error("Error in handleSend:", error);
    } finally {
      setIsThinking(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file || !user || isUploading || isThinking) return;

    const title = window.prompt("Enter a title for this transcript:");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("session_id", sessionId);
    formData.append("user_id", user.$id);
    formData.append("title", title || file.name);  // Use file name as default title

    setIsUploading(true);
    const res = await fetch("http://localhost:8000/transcripts", {
      method: "POST",
      body: formData,
    });
    setIsUploading(false);

    const data = await res.json();
    if (res.ok) {
      if (onTranscriptUpload) onTranscriptUpload();  // Refresh transcripts after upload
    } else {
      console.error("Transcript upload failed:", data.error);
    }
  };

  const handleYouTubeLink = async () => {
    if (isUploading || isThinking) return;

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
        title: title || url,  // Use URL as default title
        youtube_url: url,  // your backend will detect this and process accordingly
      }),
    });
    setIsUploading(false);

    const data = await res.json();
    if (res.ok) {
      if (onTranscriptUpload) onTranscriptUpload();  // Refresh transcripts after upload
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
          disabled={isUploading || isThinking}
        />
        <button
          onClick={handleSend}
          className="bg-blue-500 text-white px-4 rounded"
          disabled={isUploading || isThinking}
        >
          Send
        </button>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => fileInputRef.current.click()}
          className="bg-gray-700 text-white px-3 py-1 rounded"
          disabled={isUploading || isThinking}
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
          disabled={isUploading || isThinking}
        >
          Add YouTube Link
        </button>
      </div>

      {(isUploading || isThinking) && (
        <div className="text-sm text-gray-600 italic mt-2">
          {isUploading ? "Transcribing... This may take a moment." : "Thinking..."}
        </div>
      )}
    </div>
  );
};

export default ChatInput;

// This component renders an input field and a send button.
// It handles sending messages to the backend and updating the chat.
// It takes `sessionId` and `onNewMessage` as props to manage the chat state and session context.