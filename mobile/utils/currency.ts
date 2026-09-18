/**
 * Formatage des montants en FCFA (ex. "12 450 000 FCFA"), sans decimales
 * (le FCFA n'a pas de sous-unite courante), avec espace comme separateur
 * de milliers.
 */
export function formatFcfa(amount: number | null | undefined): string {
  if (amount === null || amount === undefined || Number.isNaN(amount)) {
    return "-";
  }
  const rounded = Math.round(amount);
  const formatted = rounded.toLocaleString("fr-FR").replace(/ /g, " ");
  return `${formatted} FCFA`;
}
