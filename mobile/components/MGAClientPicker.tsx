import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";

import { colors, radius, spacing, typography } from "@/utils/theme";
import type { ClientSummary } from "@/types/client";

/**
 * Selecteur de client reutilise par le futur module Devis (Sprint 2).
 * En Sprint 1, seule la liste/recherche clients existe (voir app/clients/) ;
 * ce composant en est une variante compacte, sans logique de creation.
 */
interface MGAClientPickerProps {
  clients: ClientSummary[];
  selectedId?: string;
  onSelect: (client: ClientSummary) => void;
}

export function MGAClientPicker({ clients, selectedId, onSelect }: MGAClientPickerProps) {
  return (
    <FlatList
      data={clients}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => (
        <Pressable
          onPress={() => onSelect(item)}
          style={[styles.row, item.id === selectedId && styles.rowSelected]}
        >
          <Text style={styles.name}>{item.name}</Text>
          {item.city ? <Text style={styles.city}>{item.city}</Text> : null}
        </Pressable>
      )}
    />
  );
}

const styles = StyleSheet.create({
  row: {
    padding: spacing.md,
    borderRadius: radius.sm,
    borderWidth: 1,
    borderColor: colors.border,
    marginBottom: spacing.xs,
  },
  rowSelected: { borderColor: colors.primary, backgroundColor: colors.primaryLight },
  name: { ...typography.body, color: colors.text },
  city: { ...typography.caption, color: colors.textMuted },
});
