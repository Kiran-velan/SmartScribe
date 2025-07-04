import React from "react";
import Sidebar from "../components/Sidebar";
import ChatPanel from "../components/ChatPanel";

const Chat = () => {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <ChatPanel />
    </div>
  );
};

export default Chat;