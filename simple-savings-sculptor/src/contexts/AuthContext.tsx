
import React, { createContext, useContext, useState, useEffect } from "react";

interface User {
  id: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
}, []);

  const login = async (email: string, password: string) => {
    try {
        const response = await fetch("http://127.0.0.1:8001/auth", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });
        const data = await response.json();
        if (response.ok) {
            const user = { id: data.id, email };
            console.log('user debugging', user);
            setUser(user);
            localStorage.setItem("user", JSON.stringify(user));
            return user; // Return the user object
        } else {
            console.error(data.detail);
            return null;
        }
    } catch (error) {
        console.error("Login error:", error);
        return null;
    }
};


const register = async (email: string, password: string) => {
  try {
      const response = await fetch("http://127.0.0.1:8001/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (response.ok) {
          const user = { id: data.id, email };
          console.log('user debugging', user);
          setUser(user);
          localStorage.setItem("user", JSON.stringify(user));
          return user; // Return the user object
      } else {
          console.error(data.detail);
          return null;
      }
  } catch (error) {
      console.error("Registration error:", error);
      return null;
  }
};



  const logout = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
