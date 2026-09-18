import { useState } from "react";
import { FlatList, Pressable, StyleSheet, Text, View } from "react-native";
import { useRouter } from "expo-router";

import { MGAErrorState } from "@/components/MGAErrorState";
import { MGAInput } from "@/components/MGAInput";
import { MGALoader } from "@/components/MGALoader";
import { MGAMoney } from "@/components/MGAMoney";
import { useProductSearch } from "@/hooks/useProducts";
import type { ProductSummary } from "@/types/product";
import { colors, spacing, typography } from "@/utils/theme";

export default function ProductsScreen() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const { data, isLoading, isError, refetch } = useProductSearch(query);

  return (
    <View style={styles.container}>
      <View style={styles.searchBar}>
        <MGAInput
          placeholder="Rechercher un produit (reference, designation)"
          value={query}
          onChangeText={setQuery}
          autoCapitalize="none"
        />
      </View>

      {isLoading ? <MGALoader /> : null}
      {isError ? <MGAErrorState onRetry={refetch} /> : null}

      <FlatList
        data={data?.items ?? []}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.list}
        renderItem={({ item }) => (
          <ProductRow product={item} onPress={() => router.push(`/products/${item.id}`)} />
        )}
        ListEmptyComponent={
          !isLoading ? <Text style={styles.empty}>Aucun produit trouve.</Text> : null
        }
      />
    </View>
  );
}

function ProductRow({ product, onPress }: { product: ProductSummary; onPress: () => void }) {
  return (
    <Pressable onPress={onPress} style={styles.row}>
      <View style={styles.rowInfo}>
        <Text style={styles.ref}>{product.ref}</Text>
        <Text style={styles.label}>{product.label}</Text>
        {product.stock !== null ? (
          <Text style={styles.meta}>Stock : {product.stock}</Text>
        ) : null}
      </View>
      <MGAMoney amount={product.sale_price} size="body" />
    </Pressable>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  searchBar: { padding: spacing.md },
  list: { paddingHorizontal: spacing.md, paddingBottom: spacing.lg, gap: spacing.xs },
  row: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: colors.surface,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.border,
    padding: spacing.md,
  },
  rowInfo: { flex: 1, marginRight: spacing.sm },
  ref: { ...typography.caption, color: colors.textMuted },
  label: { ...typography.body, color: colors.text },
  meta: { ...typography.caption, color: colors.textMuted, marginTop: 2 },
  empty: { ...typography.body, color: colors.textMuted, textAlign: "center", marginTop: spacing.xl },
});
