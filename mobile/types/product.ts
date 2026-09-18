import type { PageMeta } from "@/types/client";

export interface ProductSummary {
  id: string;
  ref: string;
  label: string;
  category: string | null;
  stock: number | null;
  sale_price: number | null;
  vat_rate: number | null;
  purchase_price: number | null;
  margin_amount: number | null;
  margin_percent: number | null;
}

export interface ProductDetail extends ProductSummary {
  description: string | null;
  unit: string | null;
  brand: string | null;
}

export interface ProductListResponse {
  items: ProductSummary[];
  meta: PageMeta;
}
