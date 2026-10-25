from typing import Any, Literal


RepairType = Literal["Косметический", "Капитальный"]

MATERIAL_RATES: dict[RepairType, dict[str, float]] = {
    "Косметический": {
        "cement": 0.5,
        "cable": 2,
        "plaster": 1.2,
        "primer": 0.2,
        "drywall": 0.08,
    },
    "Капитальный": {
        "cement": 0.8,
        "cable": 3.5,
        "plaster": 2.5,
        "primer": 0.35,
        "drywall": 0.18,
    },
}


def calculate_estimate(
    area_sqm: float,
    repair_type: RepairType,
    materials: list[dict[str, Any]],
) -> dict[str, Any]:
    material_details = []
    for material in materials:
        quantity = round(area_sqm * MATERIAL_RATES[repair_type][material["id"]], 2)
        prices = material["prices"]
        average_price = round(sum(prices.values()) / len(prices))
        market_totals = {
            market: round(quantity * price) for market, price in prices.items()
        }
        material_details.append(
            {
                "id": material["id"],
                "name": material["name"],
                "unit": material["unit"],
                "category": material["category"],
                "quantity": quantity,
                "average_unit_price_uzs": average_price,
                "total_uzs": round(quantity * average_price),
                "market_prices": prices,
                "market_totals_uzs": market_totals,
            }
        )

    return {
        "area_sqm": area_sqm,
        "repair_type": repair_type,
        "total_uzs": sum(item["total_uzs"] for item in material_details),
        "market_totals_uzs": {
            market: sum(item["market_totals_uzs"][market] for item in material_details)
            for market in ("Джами", "Куйлюк")
        },
        "materials": material_details,
    }
