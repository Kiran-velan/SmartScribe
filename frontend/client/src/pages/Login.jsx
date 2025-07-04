import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Login = () => {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      await login(email, password);
      navigate('/chat'); // Only navigate if login succeeds
    } catch (err) {
      alert("Login failed: " + err.message);
    }
  };

  const handleRegister = async () => {
    try {
      await register(email, password); // context handles auto login too
      navigate("/chat");
    } catch (err) {
      alert("Register failed: " + err.message);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-6 rounded shadow w-96">
        <h1 className="text-2xl mb-4 text-center font-semibold">
          {isRegister ? "Register for SmartScribe" : "SmartScribe Login"}
        </h1>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 mb-3 border rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 mb-3 border rounded"
        />
        <button
          onClick={isRegister ? handleRegister : handleLogin}
          className="w-full bg-blue-500 text-white py-2 rounded mb-2"
        >
          {isRegister ? "Register" : "Login"}
        </button>
        <p
          className="text-sm text-blue-600 text-center cursor-pointer"
          onClick={() => setIsRegister(!isRegister)}
        >
          {isRegister
            ? "Already have an account? Login"
            : "New user? Register here"}
        </p>
      </div>
    </div>
  );
};

export default Login;
