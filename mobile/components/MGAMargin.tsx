import { StyleSheet, Text, View } from "react-native";

import { colors, spacing, typography } from "@/utils/theme";
import { formatFcfa } from "@/utils/currency";

/**
 * Affiche la marge (montant + pourcentage) d'une ligne de devis/produit.
 * Ne doit etre monte que si l'utilisateur a la permission "margins:view"
 * (le backend ne renvoie de toute facon pas ces champs sinon).
 */
interface MGAMarginProps {
  amount: number | null;
  percent: number | null;
}

export function MGAMargin({ amount, percent }: MGAMarginProps) {
  if (amount === null || percent === null) return null;
  return (
    <View style={styles.container}>
      <Text style={styles.label}>Marge</Text>
      <Text style={styles.value}>
        {formatFcfa(amount)} ({percent.toFixed(1)}%)
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: "row", justifyContent: "space-between" },
  label: { ...typography.caption, color: colors.textMuted },
  value: { ...typography.caption, color: colors.primary, fontWeight: "600" },
});
