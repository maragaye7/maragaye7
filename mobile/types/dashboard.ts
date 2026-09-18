export type DashboardPeriod = "today" | "month" | "year";

export interface DashboardSummary {
  period: DashboardPeriod;
  revenue: number;
  proposals_pending: number;
  proposals_accepted: number;
  invoices_pending: number;
  amount_to_collect: number;
  active_orders: number;
  active_projects: number;
  currency: string;
}
