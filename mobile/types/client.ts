export interface ClientContact {
  id: string;
  full_name: string;
  phone: string | null;
  email: string | null;
  role: string | null;
}

export interface ClientSummary {
  id: string;
  name: string;
  email: string | null;
  phone: string | null;
  city: string | null;
  is_customer: boolean;
  is_supplier: boolean;
}

export interface ClientDetail extends ClientSummary {
  address: string | null;
  zip_code: string | null;
  country: string | null;
  ninea: string | null;
  rccm: string | null;
  contacts: ClientContact[];
}

export interface PageMeta {
  page: number;
  limit: number;
  total: number | null;
  has_more: boolean;
}

export interface ClientListResponse {
  items: ClientSummary[];
  meta: PageMeta;
}
