export type MarketName = "Джами" | "Куйлюк";

export type EstimateMaterial = {
  id: string;
  name: string;
  unit: string;
  category: string;
  quantity: number;
  average_unit_price_uzs: number;
  total_uzs: number;
  market_prices: Record<MarketName, number>;
  market_totals_uzs: Record<MarketName, number>;
};

export type Estimate = {
  area_sqm: number;
  repair_type: "Косметический" | "Капитальный";
  total_uzs: number;
  market_totals_uzs: Record<MarketName, number>;
  materials: EstimateMaterial[];
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function calculateEstimate(
  area: number,
  repairType: Estimate["repair_type"],
): Promise<Estimate> {
  const response = await fetch(`${API_URL}/api/calculate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ area_sqm: area, repair_type: repairType }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || "Не удалось рассчитать смету");
  }

  return response.json() as Promise<Estimate>;
}
