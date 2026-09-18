import { api } from "@/services/api";
import type { ClientDetail, ClientListResponse } from "@/types/client";

export const clientService = {
  async search(query: string, page = 1, limit = 25): Promise<ClientListResponse> {
    const { data } = await api.get<ClientListResponse>("/clients", {
      params: { query: query || undefined, page, limit },
    });
    return data;
  },

  async getById(clientId: string): Promise<ClientDetail> {
    const { data } = await api.get<ClientDetail>(`/clients/${clientId}`);
    return data;
  },
};
