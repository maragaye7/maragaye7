import { api } from "@/services/api";
import type { DashboardPeriod, DashboardSummary } from "@/types/dashboard";

export const dashboardService = {
  async getSummary(period: DashboardPeriod = "month"): Promise<DashboardSummary> {
    const { data } = await api.get<DashboardSummary>("/dashboard/summary", {
      params: { period },
    });
    return data;
  },
};
