import { createContext, useContext, useEffect, useState } from "react";

import {
  fetchProfile,
  login as loginRequest,
  register as registerRequest,
  type AuthTokens,
  type LoginPayload,
  type RegisterPayload,
  type UserProfile,
} from "@/lib/account";

interface AuthContextValue {
  user: UserProfile | null;
  tokens: AuthTokens | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);
const STORAGE_KEY = "brazilian-sushi-auth";

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [tokens, setTokens] = useState<AuthTokens | null>(null);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      setIsLoading(false);
      return;
    }

    try {
      const parsed = JSON.parse(stored) as AuthTokens;
      setTokens(parsed);
      fetchProfile(parsed.access)
        .then(setUser)
        .catch(() => {
          window.localStorage.removeItem(STORAGE_KEY);
          setTokens(null);
          setUser(null);
        })
        .finally(() => setIsLoading(false));
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
      setIsLoading(false);
    }
  }, []);

  const persistTokens = (nextTokens: AuthTokens | null) => {
    setTokens(nextTokens);
    if (nextTokens) {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextTokens));
    } else {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  };

  const refreshProfile = async () => {
    if (!tokens) return;
    const profile = await fetchProfile(tokens.access);
    setUser(profile);
  };

  const login = async (payload: LoginPayload) => {
    const nextTokens = await loginRequest(payload);
    persistTokens(nextTokens);
    const profile = await fetchProfile(nextTokens.access);
    setUser(profile);
  };

  const register = async (payload: RegisterPayload) => {
    await registerRequest(payload);
    try {
      await login({ email: payload.email, password: payload.password });
    } catch {
      throw new Error("Your account was created, but automatic sign-in could not be completed. Please sign in with your new credentials.");
    }
  };

  const logout = () => {
    persistTokens(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        tokens,
        isAuthenticated: Boolean(tokens && user),
        isLoading,
        login,
        register,
        logout,
        refreshProfile,
      }}
    >
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
