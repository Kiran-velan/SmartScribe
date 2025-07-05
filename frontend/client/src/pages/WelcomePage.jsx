import React from "react";
import { SparklesIcon } from "@heroicons/react/24/outline";

const WelcomePage = () => {
  return (
    <div className="w-full h-full flex flex-col justify-center items-center text-center bg-gradient-to-br from-white to-blue-50 px-4">
      <div className="flex items-center gap-2 mb-6">
        <SparklesIcon className="h-8 w-8 text-blue-500" />
        <h1 className="text-4xl font-bold text-blue-600">
          Welcome back to SmartScribe
        </h1>
      </div>

      <p className="max-w-2xl text-gray-700 text-lg mb-4">
        Transcribe & summarize your <span className="font-medium">audio</span>, <span className="font-medium">video</span>, or <span className="font-medium">YouTube</span> content in seconds.
      </p>

      <div className="text-sm text-gray-600">
        <p className="mb-1">➡️ Click <span className="font-semibold text-blue-600">“New Chat”</span> to start a fresh session.</p>
        <p>🗂️ Or pick a session from the sidebar to continue where you left off.</p>
      </div>
    </div>
  );
};

export default WelcomePage;
