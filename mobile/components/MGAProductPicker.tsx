import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";

import { MGAMoney } from "@/components/MGAMoney";
import { colors, radius, spacing, typography } from "@/utils/theme";
import type { ProductSummary } from "@/types/product";

/**
 * Selecteur de produit reutilise par le futur module Devis (Sprint 2).
 */
interface MGAProductPickerProps {
  products: ProductSummary[];
  onSelect: (product: ProductSummary) => void;
}

export function MGAProductPicker({ products, onSelect }: MGAProductPickerProps) {
  return (
    <FlatList
      data={products}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <Pressable onPress={() => onSelect(item)} style={styles.row}>
          <View style={styles.info}>
            <Text style={styles.ref}>{item.ref}</Text>
            <Text style={styles.label}>{item.label}</Text>
          </View>
          <MGAMoney amount={item.sale_price} size="body" />
        </Pressable>
      )}
    />
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    padding: spacing.md,
    borderRadius: radius.sm,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: spacing.xs,
  },
  info: { flex: 1, marginRight: spacing.sm },
  ref: { ...typography.caption, color: colors.textMuted },
  label: { ...typography.body, color: colors.text },
});
