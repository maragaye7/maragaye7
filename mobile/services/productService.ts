import { api } from "@/services/api";
import type { ProductDetail, ProductListResponse } from "@/types/product";

export const productService = {
  async search(query: string, category?: string, page = 1, limit = 25): Promise<ProductListResponse> {
    const { data } = await api.get<ProductListResponse>("/products", {
      params: { query: query || undefined, category: category || undefined, page, limit },
    });
    return data;
  },

  async getById(productId: string): Promise<ProductDetail> {
    const { data } = await api.get<ProductDetail>(`/products/${productId}`);
    return data;
  },
};
