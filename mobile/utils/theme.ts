/**
 * Identite visuelle MGA Mobile (ARCHITECTURE.md section 16 du brief) :
 * moderne, sobre, institutionnel/technique/energie, vert MG Assistance,
 * fond clair, cartes aux coins legerement arrondis, tres lisible en plein
 * soleil sur chantier (contrastes forts, tailles de police genereuses).
 */

export const colors = {
  primary: "#1F7A4D", // vert MG Assistance
  primaryDark: "#155C39",
  primaryLight: "#E6F3EC",

  background: "#F4F7F5",
  surface: "#FFFFFF",

  text: "#12241A",
  textMuted: "#5B6A62",
  border: "#DCE5E0",

  success: "#1F7A4D",
  warning: "#B8860B",
  danger: "#B3261E",
  info: "#2E6F8E",
} as const;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
} as const;

export const radius = {
  sm: 8,
  md: 12,
  lg: 16,
} as const;

export const typography = {
  title: { fontSize: 24, fontWeight: "700" as const },
  subtitle: { fontSize: 18, fontWeight: "600" as const },
  body: { fontSize: 16, fontWeight: "400" as const },
  caption: { fontSize: 13, fontWeight: "400" as const },
  money: { fontSize: 20, fontWeight: "700" as const },
};
