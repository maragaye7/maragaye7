import * as SecureStore from "expo-secure-store";
import { create } from "zustand";

import type { CurrentUser, TokenPair } from "@/types/auth";

const ACCESS_TOKEN_KEY = "mga_access_token";
const REFRESH_TOKEN_KEY = "mga_refresh_token";

interface AuthState {
  accessToken: string | null;
  refreshToken: string | null;
  user: CurrentUser | null;
  isHydrated: boolean;
  hydrate: () => Promise<void>;
  setSession: (tokens: TokenPair, user: CurrentUser | null) => Promise<void>;
  setUser: (user: CurrentUser) => void;
  setAccessToken: (accessToken: string) => Promise<void>;
  clear: () => Promise<void>;
}

/**
 * Etat d'authentification global. Les tokens ne sont JAMAIS stockes en
 * clair dans AsyncStorage : `expo-secure-store` utilise le Keychain iOS /
 * Keystore Android.
 */
export const useAuthStore = create<AuthState>((set) => ({
  accessToken: null,
  refreshToken: null,
  user: null,
  isHydrated: false,

  hydrate: async () => {
    const [accessToken, refreshToken] = await Promise.all([
      SecureStore.getItemAsync(ACCESS_TOKEN_KEY),
      SecureStore.getItemAsync(REFRESH_TOKEN_KEY),
    ]);
    set({ accessToken, refreshToken, isHydrated: true });
  },

  setSession: async (tokens, user) => {
    await Promise.all([
      SecureStore.setItemAsync(ACCESS_TOKEN_KEY, tokens.access_token),
      SecureStore.setItemAsync(REFRESH_TOKEN_KEY, tokens.refresh_token),
    ]);
    set({ accessToken: tokens.access_token, refreshToken: tokens.refresh_token, user });
  },

  setUser: (user) => set({ user }),

  setAccessToken: async (accessToken) => {
    await SecureStore.setItemAsync(ACCESS_TOKEN_KEY, accessToken);
    set({ accessToken });
  },

  clear: async () => {
    await Promise.all([
      SecureStore.deleteItemAsync(ACCESS_TOKEN_KEY),
      SecureStore.deleteItemAsync(REFRESH_TOKEN_KEY),
    ]);
    set({ accessToken: null, refreshToken: null, user: null });
  },
}));
