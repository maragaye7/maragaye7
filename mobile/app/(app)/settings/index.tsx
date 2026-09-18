import { StyleSheet, Text, View } from "react-native";

import { MGAButton } from "@/components/MGAButton";
import { MGACard } from "@/components/MGACard";
import { useCurrentUser, useLogout } from "@/hooks/useAuth";
import { colors, spacing, typography } from "@/utils/theme";

export default function SettingsScreen() {
  const { data: user } = useCurrentUser();
  const logout = useLogout();

  return (
    <View style={styles.container}>
      <MGACard style={styles.card}>
        <Text style={styles.name}>{user?.full_name ?? "..."}</Text>
        <Text style={styles.meta}>{user?.email}</Text>
        <Text style={styles.role}>{user?.role}</Text>
      </MGACard>

      <MGAButton
        label="Se deconnecter"
        variant="danger"
        loading={logout.isPending}
        onPress={() => logout.mutate()}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: spacing.md, gap: spacing.md },
  card: { gap: spacing.xs },
  name: { ...typography.subtitle, color: colors.text },
  meta: { ...typography.caption, color: colors.textMuted },
  role: { ...typography.caption, color: colors.primary, fontWeight: "600" },
});
