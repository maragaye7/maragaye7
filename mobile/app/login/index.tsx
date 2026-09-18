import { useState } from "react";
import { Image, KeyboardAvoidingView, Platform, StyleSheet, Text, View } from "react-native";
import { Redirect } from "expo-router";

import { MGAButton } from "@/components/MGAButton";
import { MGAInput } from "@/components/MGAInput";
import { useLogin } from "@/hooks/useAuth";
import { useAuthStore } from "@/stores/authStore";
import { colors, spacing, typography } from "@/utils/theme";

export default function LoginScreen() {
  const accessToken = useAuthStore((s) => s.accessToken);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const login = useLogin();

  if (accessToken) {
    return <Redirect href="/dashboard" />;
  }

  const errorMessage =
    login.isError && (login.error as { response?: { status?: number } })?.response?.status === 401
      ? "Email ou mot de passe invalide."
      : login.isError
        ? "Connexion impossible. Verifiez votre reseau et reessayez."
        : undefined;

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.header}>
        <Text style={styles.title}>MGA Mobile</Text>
        <Text style={styles.subtitle}>MG Assistance SUARL</Text>
      </View>

      <View style={styles.form}>
        <MGAInput
          label="Email"
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          keyboardType="email-address"
          placeholder="prenom.nom@mgassistances.com"
        />
        <MGAInput
          label="Mot de passe"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          placeholder="********"
        />
        {errorMessage ? <Text style={styles.error}>{errorMessage}</Text> : null}
        <MGAButton
          label="Se connecter"
          loading={login.isPending}
          disabled={!email || !password}
          onPress={() => login.mutate({ email, password })}
        />
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, justifyContent: "center", padding: spacing.lg },
  header: { alignItems: "center", marginBottom: spacing.xl },
  title: { ...typography.title, color: colors.primary },
  subtitle: { ...typography.body, color: colors.textMuted },
  form: { gap: spacing.md },
  error: { color: colors.danger, ...typography.caption },
});
