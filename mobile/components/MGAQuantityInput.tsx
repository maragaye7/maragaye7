import { Pressable, StyleSheet, Text, View } from "react-native";

import { colors, radius, spacing, typography } from "@/utils/theme";

/**
 * Stepper de quantite reutilise par le futur module Devis (Sprint 2).
 */
interface MGAQuantityInputProps {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
}

export function MGAQuantityInput({ value, onChange, min = 0, max = 9999 }: MGAQuantityInputProps) {
  return (
    <View style={styles.container}>
      <Pressable
        accessibilityRole="button"
        style={styles.button}
        onPress={() => onChange(Math.max(min, value - 1))}
      >
        <Text style={styles.buttonLabel}>-</Text>
      </Pressable>
      <Text style={styles.value}>{value}</Text>
      <Pressable
        accessibilityRole="button"
        style={styles.button}
        onPress={() => onChange(Math.min(max, value + 1))}
      >
        <Text style={styles.buttonLabel}>+</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: "row", alignItems: "center", gap: spacing.sm },
  button: {
    width: 32,
    height: 32,
    borderRadius: radius.sm,
    backgroundColor: colors.primaryLight,
    alignItems: "center",
    justifyContent: "center",
  },
  buttonLabel: { ...typography.subtitle, color: colors.primary },
  value: { ...typography.body, minWidth: 32, textAlign: "center" },
});
