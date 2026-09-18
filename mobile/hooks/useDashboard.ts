import { useQuery } from "@tanstack/react-query";

import { dashboardService } from "@/services/dashboardService";
import type { DashboardPeriod } from "@/types/dashboard";

export function useDashboardSummary(period: DashboardPeriod = "month") {
  return useQuery({
    queryKey: ["dashboard", "summary", period],
    queryFn: () => dashboardService.getSummary(period),
    staleTime: 60 * 1000,
  });
}
