import { StyleSheet, Text, View } from "react-native";

import { colors, radius, spacing, typography } from "@/utils/theme";

export type MGAStatus = "success" | "warning" | "danger" | "info" | "neutral";

interface MGAStatusBadgeProps {
  label: string;
  status?: MGAStatus;
}

const STATUS_COLOR: Record<MGAStatus, string> = {
  success: colors.success,
  warning: colors.warning,
  danger: colors.danger,
  info: colors.info,
  neutral: colors.textMuted,
};

export function MGAStatusBadge({ label, status = "neutral" }: MGAStatusBadgeProps) {
  const tint = STATUS_COLOR[status];
  return (
    <View style={[styles.badge, { borderColor: tint, backgroundColor: `${tint}1A` }]}>
      <Text style={[styles.label, { color: tint }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  badge: {
    alignSelf: "flex-start",
    borderWidth: 1,
    borderRadius: radius.lg,
    paddingHorizontal: spacing.sm,
    paddingVertical: 2,
  },
  label: { ...typography.caption, fontWeight: "600" },
});
