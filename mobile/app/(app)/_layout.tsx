import { Redirect, Tabs } from "expo-router";

import { useAuthStore } from "@/stores/authStore";
import { colors } from "@/utils/theme";

export default function AppLayout() {
  const accessToken = useAuthStore((s) => s.accessToken);

  if (!accessToken) {
    return <Redirect href="/login" />;
  }

  return (
    <Tabs
      screenOptions={{
        headerTintColor: colors.text,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textMuted,
      }}
    >
      <Tabs.Screen name="dashboard/index" options={{ title: "Tableau de bord" }} />
      <Tabs.Screen name="clients/index" options={{ title: "Clients" }} />
      <Tabs.Screen name="clients/[id]" options={{ href: null, title: "Fiche client" }} />
      <Tabs.Screen name="products/index" options={{ title: "Catalogue" }} />
      <Tabs.Screen name="products/[id]" options={{ href: null, title: "Fiche produit" }} />
      <Tabs.Screen name="settings/index" options={{ title: "Reglages" }} />
    </Tabs>
  );
}
