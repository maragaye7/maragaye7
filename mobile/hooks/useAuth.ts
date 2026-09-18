import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { authService } from "@/services/authService";
import { useAuthStore } from "@/stores/authStore";

export function useLogin() {
  const setSession = useAuthStore((s) => s.setSession);
  const setUser = useAuthStore((s) => s.setUser);

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      authService.login(email, password),
    onSuccess: async (tokens) => {
      await setSession(tokens, null);
      const user = await authService.me();
      setUser(user);
    },
  });
}

export function useCurrentUser() {
  const accessToken = useAuthStore((s) => s.accessToken);
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: authService.me,
    enabled: !!accessToken,
    staleTime: 5 * 60 * 1000,
  });
}

export function useLogout() {
  const { refreshToken, clear } = useAuthStore();
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      if (refreshToken) {
        await authService.logout(refreshToken);
      }
    },
    onSettled: async () => {
      await clear();
      queryClient.clear();
    },
  });
}
