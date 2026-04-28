from __future__ import annotations

from pathlib import Path

import pandas as pd


def build_metrics(raw_orders_path: Path, processed_dir: Path) -> dict[str, Path]:
    processed_dir.mkdir(parents=True, exist_ok=True)

    orders = pd.read_csv(raw_orders_path, parse_dates=["order_date"])
    orders["month"] = orders["order_date"].dt.to_period("M").astype(str)
    orders["gross_revenue"] = orders["quantity"] * orders["unit_price"]
    orders["net_revenue"] = orders["gross_revenue"] * (1 - orders["discount_pct"])
    orders["return_loss"] = orders["net_revenue"] * orders["returned"]

    monthly_region = (
        orders.groupby(["month", "region"], as_index=False)
        .agg(
            orders=("order_id", "count"),
            units=("quantity", "sum"),
            gross_revenue=("gross_revenue", "sum"),
            net_revenue=("net_revenue", "sum"),
            return_loss=("return_loss", "sum"),
        )
        .assign(net_after_returns=lambda d: d["net_revenue"] - d["return_loss"])
        .sort_values(["month", "region"])
    )

    customer_ltv = (
        orders.groupby("customer_id", as_index=False)
        .agg(
            orders=("order_id", "count"),
            lifetime_net_revenue=("net_revenue", "sum"),
            avg_order_value=("net_revenue", "mean"),
        )
        .sort_values("lifetime_net_revenue", ascending=False)
    )

    product_performance = (
        orders.groupby(["category", "product_name"], as_index=False)
        .agg(
            units=("quantity", "sum"),
            net_revenue=("net_revenue", "sum"),
            average_discount=("discount_pct", "mean"),
            return_rate=("returned", "mean"),
        )
        .sort_values("net_revenue", ascending=False)
    )

    outputs = {
        "monthly_region_kpis": processed_dir / "monthly_region_kpis.csv",
        "customer_ltv": processed_dir / "customer_ltv.csv",
        "product_performance": processed_dir / "product_performance.csv",
    }

    monthly_region.round(2).to_csv(outputs["monthly_region_kpis"], index=False)
    customer_ltv.round(2).to_csv(outputs["customer_ltv"], index=False)
    product_performance.round(3).to_csv(outputs["product_performance"], index=False)
    return outputs
