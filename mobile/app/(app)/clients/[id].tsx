import { ScrollView, StyleSheet, Text, View } from "react-native";
import { useLocalSearchParams } from "expo-router";

import { MGACard } from "@/components/MGACard";
import { MGAErrorState } from "@/components/MGAErrorState";
import { MGALoader } from "@/components/MGALoader";
import { useClientDetail } from "@/hooks/useClients";
import { colors, spacing, typography } from "@/utils/theme";

export default function ClientDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { data, isLoading, isError, refetch } = useClientDetail(id);

  if (isLoading) return <MGALoader />;
  if (isError || !data) return <MGAErrorState onRetry={refetch} />;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{data.name}</Text>

      <MGACard style={styles.card}>
        <Field label="Adresse" value={[data.address, data.zip_code, data.city, data.country].filter(Boolean).join(", ")} />
        <Field label="Telephone" value={data.phone} />
        <Field label="Email" value={data.email} />
        <Field label="NINEA" value={data.ninea} />
        <Field label="RCCM" value={data.rccm} />
      </MGACard>

      <Text style={styles.sectionTitle}>Contacts ({data.contacts.length})</Text>
      {data.contacts.length === 0 ? (
        <Text style={styles.empty}>Aucun contact enregistre.</Text>
      ) : (
        data.contacts.map((contact) => (
          <MGACard key={contact.id} style={styles.card}>
            <Text style={styles.contactName}>{contact.full_name}</Text>
            <Text style={styles.meta}>{[contact.phone, contact.email].filter(Boolean).join(" - ")}</Text>
          </MGACard>
        ))
      )}

      <Text style={styles.sectionTitle}>Devis, commandes, factures, projets</Text>
      <Text style={styles.empty}>Disponible a partir du Sprint 2 (voir ARCHITECTURE.md).</Text>
    </ScrollView>
  );
}

function Field({ label, value }: { label: string; value: string | null | undefined }) {
  if (!value) return null;
  return (
    <View style={styles.field}>
      <Text style={styles.fieldLabel}>{label}</Text>
      <Text style={styles.fieldValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.md, gap: spacing.md },
  title: { ...typography.title, color: colors.text },
  card: { gap: spacing.sm },
  field: { gap: 2 },
  fieldLabel: { ...typography.caption, color: colors.textMuted },
  fieldValue: { ...typography.body, color: colors.text },
  sectionTitle: { ...typography.subtitle, color: colors.text, marginTop: spacing.sm },
  contactName: { ...typography.body, color: colors.text, fontWeight: "600" },
  meta: { ...typography.caption, color: colors.textMuted },
  empty: { ...typography.body, color: colors.textMuted },
});
