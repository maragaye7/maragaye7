import { StyleSheet, Text, View } from "react-native";

import { MGAButton } from "@/components/MGAButton";
import { colors, spacing, typography } from "@/utils/theme";

interface MGAErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export function MGAErrorState({
  message = "Une erreur est survenue. Verifiez votre connexion et reessayez.",
  onRetry,
}: MGAErrorStateProps) {
  return (
    <View style={styles.container}>
      <Text style={styles.message}>{message}</Text>
      {onRetry ? <MGAButton label="Reessayer" onPress={onRetry} variant="secondary" /> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    gap: spacing.md,
    padding: spacing.lg,
  },
  message: { ...typography.body, color: colors.textMuted, textAlign: "center" },
});
