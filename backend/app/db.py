import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator


DATABASE_PATH = Path(
    os.getenv("STROYFIX_DATABASE_PATH", str(Path(__file__).resolve().parents[1] / "stroyfix.db"))
)

SEED_MATERIALS = (
    ("cement", "Цемент М400", "мешок 50 кг", "Черновые материалы", 65000, 67000),
    ("cable", "Кабель медный", "м", "Электрика", 8500, 9000),
    ("plaster", "Штукатурка гипсовая", "кг", "Черновые материалы", 2600, 2800),
    ("primer", "Грунтовка глубокого проникновения", "л", "Черновые материалы", 12000, 13000),
    ("drywall", "Гипсокартон 12,5 мм", "лист", "Отделочные материалы", 85000, 88000),
)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS materials (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                unit TEXT NOT NULL,
                category TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS market_prices (
                material_id TEXT NOT NULL REFERENCES materials(id),
                market TEXT NOT NULL,
                price_uzs INTEGER NOT NULL CHECK (price_uzs > 0),
                PRIMARY KEY (material_id, market)
            )
            """
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO materials (id, name, unit, category)
            VALUES (?, ?, ?, ?)
            """,
            [(row[0], row[1], row[2], row[3]) for row in SEED_MATERIALS],
        )
        connection.executemany(
            """
            INSERT OR IGNORE INTO market_prices (material_id, market, price_uzs)
            VALUES (?, ?, ?)
            """,
            [
                (material_id, market, price)
                for material_id, _, _, _, jami_price, kuylyuk_price in SEED_MATERIALS
                for market, price in (("Джами", jami_price), ("Куйлюк", kuylyuk_price))
            ],
        )


def get_materials() -> list[dict[str, Any]]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT materials.id, materials.name, materials.unit, materials.category,
                   market_prices.market, market_prices.price_uzs
            FROM materials
            JOIN market_prices ON market_prices.material_id = materials.id
            ORDER BY materials.id, market_prices.market
            """
        ).fetchall()

    materials: dict[str, dict[str, Any]] = {}
    for row in rows:
        item = materials.setdefault(
            row["id"],
            {
                "id": row["id"],
                "name": row["name"],
                "unit": row["unit"],
                "category": row["category"],
                "prices": {},
            },
        )
        item["prices"][row["market"]] = row["price_uzs"]
    return list(materials.values())
