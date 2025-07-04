import React, { useState } from "react";
import { account } from "./appwrite";

const Auth = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async () => {
    try {
      await account.create("unique()", email, password);
      await handleLogin(); // Auto login after register
    } catch (err) {
      alert("Register Error: " + err.message);
    }
  };

  const handleLogin = async () => {
    try {
      await account.createEmailPasswordSession(email, password);
      const user = await account.get();
      onLogin(user);
    } catch (err) {
      alert("Login Error: " + err.message);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Login / Register</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      /><br /><br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      /><br /><br />
      <button onClick={handleLogin}>Login</button>{" "}
      <button onClick={handleRegister}>Register</button>
    </div>
  );
};

export default Auth;
