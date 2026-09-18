import { Text, type TextStyle } from "react-native";

import { colors, typography } from "@/utils/theme";
import { formatFcfa } from "@/utils/currency";

interface MGAMoneyProps {
  amount: number | null | undefined;
  size?: "body" | "money" | "title";
  color?: string;
  style?: TextStyle;
}

export function MGAMoney({ amount, size = "money", color = colors.text, style }: MGAMoneyProps) {
  return <Text style={[typography[size], { color }, style]}>{formatFcfa(amount)}</Text>;
}
