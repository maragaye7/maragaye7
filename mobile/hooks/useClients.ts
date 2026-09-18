import { useQuery } from "@tanstack/react-query";

import { clientService } from "@/services/clientService";

export function useClientSearch(query: string, page = 1) {
  return useQuery({
    queryKey: ["clients", "search", query, page],
    queryFn: () => clientService.search(query, page),
    // Les resultats recents restent affiches hors ligne (cf. strategie
    // offline, ARCHITECTURE.md section 7) grace a ce staleTime genereux.
    staleTime: 60 * 1000,
  });
}

export function useClientDetail(clientId: string | undefined) {
  return useQuery({
    queryKey: ["clients", "detail", clientId],
    queryFn: () => clientService.getById(clientId as string),
    enabled: !!clientId,
  });
}
