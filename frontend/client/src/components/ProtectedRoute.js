import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) return <p>Loading...</p>;

  return user ? children : <Navigate to="/login" replace />;  // if user exists, render children; otherwise redirect to login
};

export default ProtectedRoute;
// This component checks if the user is authenticated before rendering the protected routes. In App.js, we configure it to wrap around the Chat and NewSession components.
// If the user is not authenticated, it redirects them to the login page.
// It uses the `useAuth` hook to access the authentication state and loading status.