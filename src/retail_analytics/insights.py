from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_portfolio_summary(processed_dir: Path, output_path: Path) -> Path:
    monthly = pd.read_csv(processed_dir / "monthly_region_kpis.csv")
    ltv = pd.read_csv(processed_dir / "customer_ltv.csv")
    products = pd.read_csv(processed_dir / "product_performance.csv")

    total_net = monthly["net_after_returns"].sum()
    best_month = (
        monthly.groupby("month", as_index=False)["net_after_returns"].sum().sort_values(
            "net_after_returns", ascending=False
        )
    ).iloc[0]
    top_region = (
        monthly.groupby("region", as_index=False)["net_after_returns"].sum().sort_values(
            "net_after_returns", ascending=False
        )
    ).iloc[0]
    top_product = products.iloc[0]
    top_customer = ltv.iloc[0]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(
            [
                "# Portfolio Summary",
                "",
                "## Executive Highlights",
                f"- Total net revenue after returns: ${total_net:,.2f}",
                f"- Best month: {best_month['month']} (${best_month['net_after_returns']:,.2f})",
                f"- Top region: {top_region['region']} (${top_region['net_after_returns']:,.2f})",
                f"- Top product by net revenue: {top_product['product_name']} (${top_product['net_revenue']:,.2f})",
                (
                    "- Highest value customer: "
                    f"{int(top_customer['customer_id'])} "
                    f"(${top_customer['lifetime_net_revenue']:,.2f} lifetime net)"
                ),
                "",
                "## Interpretation",
                "- This synthetic portfolio dataset shows stable multi-region demand with concentrated product winners.",
                "- Return-loss monitoring helps estimate true realized revenue instead of gross sales only.",
                "- The customer LTV table can support segmentation and retention campaign design.",
            ]
        ),
        encoding="utf-8",
    )
    return output_path
