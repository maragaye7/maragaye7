import { api } from "@/services/api";
import type { CurrentUser, TokenPair } from "@/types/auth";

export const authService = {
  async login(email: string, password: string): Promise<TokenPair> {
    const { data } = await api.post<TokenPair>("/auth/login", { email, password });
    return data;
  },

  async me(): Promise<CurrentUser> {
    const { data } = await api.get<CurrentUser>("/auth/me");
    return data;
  },

  async logout(refreshToken: string): Promise<void> {
    await api.post("/auth/logout", { refresh_token: refreshToken });
  },
};
