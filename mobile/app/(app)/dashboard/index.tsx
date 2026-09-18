import { useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";

import { MGACard } from "@/components/MGACard";
import { MGAErrorState } from "@/components/MGAErrorState";
import { MGALoader } from "@/components/MGALoader";
import { MGAMoney } from "@/components/MGAMoney";
import { useCurrentUser } from "@/hooks/useAuth";
import { useDashboardSummary } from "@/hooks/useDashboard";
import type { DashboardPeriod } from "@/types/dashboard";
import { colors, spacing, typography } from "@/utils/theme";

const PERIODS: { value: DashboardPeriod; label: string }[] = [
  { value: "today", label: "Aujourd'hui" },
  { value: "month", label: "Mois" },
  { value: "year", label: "Annee" },
];

export default function DashboardScreen() {
  const router = useRouter();
  const { data: user } = useCurrentUser();
  const [period, setPeriod] = useState<DashboardPeriod>("month");
  const { data, isLoading, isError, refetch } = useDashboardSummary(period);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.greeting}>Bonjour{user ? `, ${user.full_name}` : ""}</Text>

      <View style={styles.periodRow}>
        {PERIODS.map((p) => (
          <Pressable
            key={p.value}
            onPress={() => setPeriod(p.value)}
            style={[styles.periodChip, period === p.value && styles.periodChipActive]}
          >
            <Text style={[styles.periodLabel, period === p.value && styles.periodLabelActive]}>
              {p.label}
            </Text>
          </Pressable>
        ))}
      </View>

      {isLoading ? <MGALoader /> : null}
      {isError ? <MGAErrorState onRetry={refetch} /> : null}

      {data ? (
        <View style={styles.grid}>
          <MGACard style={styles.tile}>
            <Text style={styles.tileLabel}>Chiffre d'affaires</Text>
            <MGAMoney amount={data.revenue} />
          </MGACard>
          <MGACard style={styles.tile}>
            <Text style={styles.tileLabel}>A encaisser</Text>
            <MGAMoney amount={data.amount_to_collect} />
          </MGACard>
          <MGACard style={styles.tile}>
            <Text style={styles.tileLabel}>Devis en cours</Text>
            <Text style={styles.tileValue}>{data.proposals_pending}</Text>
          </MGACard>
          <MGACard style={styles.tile}>
            <Text style={styles.tileLabel}>Devis acceptes</Text>
            <Text style={styles.tileValue}>{data.proposals_accepted}</Text>
          </MGACard>
          <MGACard style={styles.tile}>
            <Text style={styles.tileLabel}>Factures en attente</Text>
            <Text style={styles.tileValue}>{data.invoices_pending}</Text>
          </MGACard>
          <MGACard style={styles.tile}>
            <Text style={styles.tileLabel}>Commandes actives</Text>
            <Text style={styles.tileValue}>{data.active_orders}</Text>
          </MGACard>
          <MGACard style={styles.tile}>
            <Text style={styles.tileLabel}>Projets actifs</Text>
            <Text style={styles.tileValue}>{data.active_projects}</Text>
          </MGACard>
        </View>
      ) : null}

      <Text style={styles.sectionTitle}>Actions rapides</Text>
      <View style={styles.quickActions}>
        <QuickAction label="Nouveau client" onPress={() => router.push("/clients")} />
        <QuickAction label="Catalogue produits" onPress={() => router.push("/products")} />
        <QuickAction label="Nouveau devis" disabled note="Sprint 2" />
        <QuickAction label="Nouvelle facture" disabled note="Sprint 3" />
        <QuickAction label="Nouveau projet" disabled note="Sprint 3" />
        <QuickAction label="Assistant IA" disabled note="Sprint 4" />
      </View>
    </ScrollView>
  );
}

function QuickAction({
  label,
  onPress,
  disabled,
  note,
}: {
  label: string;
  onPress?: () => void;
  disabled?: boolean;
  note?: string;
}) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={[styles.actionCard, disabled && styles.actionCardDisabled]}
    >
      <Text style={styles.actionLabel}>{label}</Text>
      {note ? <Text style={styles.actionNote}>{note}</Text> : null}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.md, gap: spacing.md },
  greeting: { ...typography.title, color: colors.text },
  periodRow: { flexDirection: "row", gap: spacing.sm },
  periodChip: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: colors.border,
  },
  periodChipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  periodLabel: { ...typography.caption, color: colors.textMuted },
  periodLabelActive: { color: "#fff", fontWeight: "600" },
  grid: { flexDirection: "row", flexWrap: "wrap", gap: spacing.sm },
  tile: { width: "47%", gap: spacing.xs },
  tileLabel: { ...typography.caption, color: colors.textMuted },
  tileValue: { ...typography.money, color: colors.text },
  sectionTitle: { ...typography.subtitle, color: colors.text, marginTop: spacing.sm },
  quickActions: { flexDirection: "row", flexWrap: "wrap", gap: spacing.sm },
  actionCard: {
    width: "47%",
    backgroundColor: colors.primaryLight,
    borderRadius: 12,
    padding: spacing.md,
  },
  actionCardDisabled: { opacity: 0.5 },
  actionLabel: { ...typography.body, color: colors.primaryDark, fontWeight: "600" },
  actionNote: { ...typography.caption, color: colors.textMuted, marginTop: 2 },
});
