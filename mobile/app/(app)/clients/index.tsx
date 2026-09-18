import { useState } from "react";
import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";

import { MGAErrorState } from "@/components/MGAErrorState";
import { MGAInput } from "@/components/MGAInput";
import { MGALoader } from "@/components/MGALoader";
import { useClientSearch } from "@/hooks/useClients";
import type { ClientSummary } from "@/types/client";
import { colors, spacing, typography } from "@/utils/theme";

export default function ClientsScreen() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const { data, isLoading, isError, refetch, isFetching } = useClientSearch(query);

  return (
    <View style={styles.container}>
      <View style={styles.searchBar}>
        <MGAInput
          placeholder="Rechercher un client (nom, email, telephone, reference)"
          value={query}
          onChangeText={setQuery}
          autoCapitalize="none"
        />
      </View>

      {isLoading && !isFetching ? <MGALoader /> : null}
      {isError ? <MGAErrorState onRetry={refetch} /> : null}

      <FlatList
        data={data?.items ?? []}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
        renderItem={({ item }) => (
          <ClientRow client={item} onPress={() => router.push(`/clients/${item.id}`)} />
        )}
        ListEmptyComponent={
          !isLoading ? <Text style={styles.empty}>Aucun client trouve.</Text> : null
        }
      />
    </View>
  );
}

function ClientRow({ client, onPress }: { client: ClientSummary; onPress: () => void }) {
  return (
    <Pressable onPress={onPress} style={styles.row}>
      <Text style={styles.name}>{client.name}</Text>
      <Text style={styles.meta}>
        {[client.phone, client.email, client.city].filter(Boolean).join(" - ") || "-"}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  searchBar: { padding: spacing.md },
  list: { paddingHorizontal: spacing.md, paddingBottom: spacing.lg, gap: spacing.xs },
  row: {
    backgroundColor: colors.surface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
  },
  name: { ...typography.subtitle, color: colors.text },
  meta: { ...typography.caption, color: colors.textMuted, marginTop: 2 },
  empty: { ...typography.body, color: colors.textMuted, textAlign: "center", marginTop: spacing.xl },
});
