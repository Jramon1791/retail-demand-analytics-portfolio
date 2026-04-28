from __future__ import annotations

from pathlib import Path

from retail_analytics.data_generator import GeneratorConfig, write_raw_orders
from retail_analytics.insights import write_portfolio_summary
from retail_analytics.pipeline import build_metrics


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    raw_dir = root / "data" / "raw"
    processed_dir = root / "data" / "processed"
    output_summary = root / "outputs" / "portfolio_summary.md"

    raw_path = write_raw_orders(raw_dir, GeneratorConfig(n_orders=6000, seed=12))
    outputs = build_metrics(raw_path, processed_dir)
    summary_path = write_portfolio_summary(processed_dir, output_summary)

    print("Pipeline complete.")
    print(f"Raw orders: {raw_path}")
    for name, path in outputs.items():
        print(f"{name}: {path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
