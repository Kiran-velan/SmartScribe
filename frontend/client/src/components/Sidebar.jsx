import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Sidebar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [sessions, setSessions] = useState([]);

  const fetchSessions = useCallback(async () => {
    try {
      const res = await fetch(`http://localhost:8000/sessions?user_id=${user.$id}`);
      const data = await res.json();
      if (res.ok) {
        setSessions(data.sessions || []);
      } else {
        console.error("Session fetch error:", data.error);
      }
    } catch (err) {
      console.error("Session fetch error:", err);
    }
  }, [user?.$id]);

  useEffect(() => {
    if (user) fetchSessions();
  }, [user, fetchSessions]);

  const handleNewChat = async () => {
    const title = window.prompt("Enter title for your new chat:");
    if (!title) return;

    try {
      const res = await fetch("http://localhost:8000/sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, user_id: user.$id }),
      });

      const data = await res.json();
      if (res.ok) {
        fetchSessions(); // refresh after new session
        navigate(`/chat/${data.session.$id}`);
      } else {
        console.error("Error creating session:", data.error);
      }
    } catch (err) {
      console.error("Failed to create new session", err);
    }
  };

  return (
    <div className="w-64 bg-gray-800 text-white p-4 flex flex-col">
      <button
        onClick={handleNewChat}
        className="bg-green-500 hover:bg-green-600 py-2 px-3 rounded mb-4"
      >
        + New Chat
      </button>

      <div className="flex-1 overflow-y-auto">
        {(sessions || []).map((s) => (
          <div
            key={s.$id}
            className="cursor-pointer py-2 px-2 hover:bg-gray-700 rounded"
            onClick={() => navigate(`/chat/${s.$id}`)}
          >
            {s.title}
          </div>
        ))}
      </div>

      <button
        onClick={logout}
        className="bg-red-500 hover:bg-red-600 py-2 px-3 rounded mt-4"
      >
        Logout
      </button>
    </div>
  );
};

export default Sidebar;
