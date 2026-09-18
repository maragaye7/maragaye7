import { ScrollView, StyleSheet, Text, View } from "react-native";
import { useLocalSearchParams } from "expo-router";

import { MGACard } from "@/components/MGACard";
import { MGAErrorState } from "@/components/MGAErrorState";
import { MGALoader } from "@/components/MGALoader";
import { MGAMargin } from "@/components/MGAMargin";
import { MGAMoney } from "@/components/MGAMoney";
import { useProductDetail } from "@/hooks/useProducts";
import { colors, spacing, typography } from "@/utils/theme";

export default function ProductDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data, isLoading, isError, refetch } = useProductDetail(id);

  if (isLoading) return <MGALoader />;
  if (isError || !data) return <MGAErrorState onRetry={refetch} />;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.ref}>{data.ref}</Text>
      <Text style={styles.title}>{data.label}</Text>

      <MGACard style={styles.card}>
        <View style={styles.priceRow}>
          <Text style={styles.priceLabel}>Prix de vente</Text>
          <MGAMoney amount={data.sale_price} />
        </View>
        {data.vat_rate !== null ? (
          <Field label="TVA" value={`${data.vat_rate}%`} />
        ) : null}
        {data.stock !== null ? <Field label="Stock" value={String(data.stock)} /> : null}
        {data.unit ? <Field label="Unite" value={data.unit} /> : null}
        <MGAMargin amount={data.margin_amount} percent={data.margin_percent} />
      </MGACard>

      {data.description ? (
        <MGACard style={styles.card}>
          <Text style={styles.sectionTitle}>Description</Text>
          <Text style={styles.description}>{data.description}</Text>
        </MGACard>
      ) : null}
    </ScrollView>
  );
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.fieldRow}>
      <Text style={styles.fieldLabel}>{label}</Text>
      <Text style={styles.fieldValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.md, gap: spacing.md },
  ref: { ...typography.caption, color: colors.textMuted },
  title: { ...typography.title, color: colors.text },
  card: { gap: spacing.sm },
  priceRow: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  priceLabel: { ...typography.body, color: colors.textMuted },
  fieldRow: { flexDirection: "row", justifyContent: "space-between" },
  fieldLabel: { ...typography.caption, color: colors.textMuted },
  fieldValue: { ...typography.caption, color: colors.text },
  sectionTitle: { ...typography.subtitle, color: colors.text },
  description: { ...typography.body, color: colors.text },
});
