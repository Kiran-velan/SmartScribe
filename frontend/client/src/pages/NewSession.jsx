import React from "react";

const NewSession = () => {
  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl font-bold mb-4">Start New SmartScribe Session</h1>
      <input type="text" placeholder="YouTube Link" className="p-2 border rounded w-80 mb-3" />
      <input type="file" accept="audio/*,video/*" className="mb-3" />
      <button className="bg-blue-500 text-white px-4 py-2 rounded">Upload & Transcribe</button>
    </div>
  );
};

export default NewSession;