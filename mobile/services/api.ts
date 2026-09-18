import * as SecureStore from "expo-secure-store";

const API_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function login(username: string, password: string) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password}),
  });
  if (!res.ok) throw new Error("Connexion refusée");
  const data = await res.json();
  await SecureStore.setItemAsync("access_token", data.access_token);
}

export async function apiGet(path: string) {
  const token = await SecureStore.getItemAsync("access_token");
  const res = await fetch(`${API_URL}${path}`, {
    headers: {Authorization: `Bearer ${token}`},
  });
  if (!res.ok) throw new Error(`Erreur API ${res.status}`);
  return res.json();
}

export async function logout() {
  await SecureStore.deleteItemAsync("access_token");
}
