// src/context/AuthContext.tsx
import { createContext, useState, useContext, ReactNode } from "react";

interface UserRole {
  isAdmin: boolean;
  isParent: boolean;
  isAccountant: boolean;
}

interface AuthContextType {
  isAuthenticated: boolean;
  userRole: UserRole | null;
  login: (accessToken: string, role: UserRole) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return !!localStorage.getItem("access_token");
  });
  const [userRole, setUserRole] = useState<UserRole | null>(() => {
    const storedRole = localStorage.getItem("user_role");
    return storedRole ? JSON.parse(storedRole) : null;
  });

  const login = (accessToken: string, role: UserRole) => {
    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("user_role", JSON.stringify(role));
    setIsAuthenticated(true);
    setUserRole(role);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_role");
    setIsAuthenticated(false);
    setUserRole(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, userRole, login, logout }}>
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
