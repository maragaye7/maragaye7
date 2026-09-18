export type UserRole = "ADMIN" | "DIRECTION" | "COMMERCIAL" | "TECHNICIEN";

export interface CurrentUser {
  id: string;
  email: string;
  full_name: string;
  role: UserRole;
  can_see_margins: boolean;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
