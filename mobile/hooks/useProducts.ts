import { useQuery } from "@tanstack/react-query";

import { productService } from "@/services/productService";

export function useProductSearch(query: string, category?: string, page = 1) {
  return useQuery({
    queryKey: ["products", "search", query, category, page],
    queryFn: () => productService.search(query, category, page),
    staleTime: 60 * 1000,
  });
}

export function useProductDetail(productId: string | undefined) {
  return useQuery({
    queryKey: ["products", "detail", productId],
    queryFn: () => productService.getById(productId as string),
    enabled: !!productId,
  });
}
