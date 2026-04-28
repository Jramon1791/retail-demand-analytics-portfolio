from pathlib import Path

import pandas as pd

from retail_analytics.data_generator import GeneratorConfig, write_raw_orders
from retail_analytics.insights import write_portfolio_summary
from retail_analytics.pipeline import build_metrics


def test_pipeline_outputs(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    summary = tmp_path / "outputs" / "portfolio_summary.md"

    raw_path = write_raw_orders(raw_dir, GeneratorConfig(n_orders=200, seed=7))
    outputs = build_metrics(raw_path, processed_dir)
    write_portfolio_summary(processed_dir, summary)

    assert raw_path.exists()
    for path in outputs.values():
        assert path.exists()
    assert summary.exists()

    monthly = pd.read_csv(outputs["monthly_region_kpis"])
    ltv = pd.read_csv(outputs["customer_ltv"])
    products = pd.read_csv(outputs["product_performance"])

    assert {"month", "region", "net_after_returns"}.issubset(monthly.columns)
    assert {"customer_id", "lifetime_net_revenue"}.issubset(ltv.columns)
    assert {"product_name", "net_revenue", "return_rate"}.issubset(products.columns)
