from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class GeneratorConfig:
    n_orders: int = 5000
    seed: int = 42
    start_date: str = "2024-01-01"
    end_date: str = "2025-12-31"


def _build_orders(config: GeneratorConfig) -> pd.DataFrame:
    rng = np.random.default_rng(config.seed)

    regions = np.array(["North", "South", "East", "West"])
    channels = np.array(["web", "mobile", "store"])
    categories = np.array(["Electronics", "Home", "Beauty", "Grocery", "Sports"])
    products = np.array(
        [
            "Smart Speaker",
            "Vacuum Cleaner",
            "Running Shoes",
            "Protein Powder",
            "Skin Serum",
            "Wireless Mouse",
            "Blender",
            "Air Fryer",
            "Yoga Mat",
            "LED Monitor",
        ]
    )

    date_range = pd.date_range(config.start_date, config.end_date, freq="D")

    df = pd.DataFrame(
        {
            "order_id": np.arange(1, config.n_orders + 1),
            "customer_id": rng.integers(1000, 2000, size=config.n_orders),
            "order_date": rng.choice(date_range, size=config.n_orders),
            "region": rng.choice(regions, size=config.n_orders, p=[0.26, 0.24, 0.25, 0.25]),
            "channel": rng.choice(channels, size=config.n_orders, p=[0.48, 0.35, 0.17]),
            "category": rng.choice(categories, size=config.n_orders),
            "product_name": rng.choice(products, size=config.n_orders),
            "quantity": rng.integers(1, 6, size=config.n_orders),
            "unit_price": rng.uniform(8, 450, size=config.n_orders).round(2),
            "discount_pct": rng.uniform(0.0, 0.25, size=config.n_orders).round(3),
            "returned": rng.choice([0, 1], size=config.n_orders, p=[0.93, 0.07]),
        }
    )
    return df.sort_values("order_date").reset_index(drop=True)


def write_raw_orders(output_dir: Path, config: GeneratorConfig | None = None) -> Path:
    config = config or GeneratorConfig()
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "orders.csv"
    _build_orders(config).to_csv(path, index=False)
    return path
