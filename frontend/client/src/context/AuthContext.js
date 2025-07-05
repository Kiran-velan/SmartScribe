import { createContext, useEffect, useState, useContext } from "react";
import { account } from "../appwrite";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUser = async () => {
    try {
      const user = await account.get();
      setUser(user);
    } catch {
      // 401 is expected if user is not logged in
      setUser(null);
    } finally {
      setLoading(false); // Mark auth check as complete
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const login = async (email, password) => {
    try {
      // First try to delete any existing session
      try {
        await account.deleteSession('current');
      } catch (error) {
        // Ignore if no session exists
      }
      
      // Then create new session
      await account.createEmailPasswordSession(email, password);
      const user = await account.get();
      setUser(user);
      return user; // Return the user object
    } catch (error) {
      console.error('Login error:', error);
      throw error; // Re-throw to handle in the Login component
    }
  };

  const register = async (email, password) => {
    await account.create("unique()", email, password);
    await login(email, password); // auto login after register
  };

  const logout = async () => {
    await account.deleteSession("current");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
