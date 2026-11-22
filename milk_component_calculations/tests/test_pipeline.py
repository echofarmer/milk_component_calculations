"""Test the whole workflow on the invented example data."""

import pandas as pd

from milk_component_calculations.pipeline import run_pipeline


def test_pipeline_saves_all_result_files(tmp_path):
    """One run writes four tables and one chart."""
    run_pipeline("data/example", str(tmp_path))

    expected_files = [
        "yields_per_milking.csv",
        "daily_totals.csv",
        "summary_by_cow.csv",
        "data_quality_report.csv",
        "daily_yields_by_cow.png",
    ]
    for file_name in expected_files:
        assert (tmp_path / file_name).exists()


def test_pipeline_counts_on_example_data(tmp_path):
    """The example data gives 16 milkings, 3 full days, and 8 reported problems."""
    run_pipeline("data/example", str(tmp_path))

    yields = pd.read_csv(tmp_path / "yields_per_milking.csv")
    daily = pd.read_csv(tmp_path / "daily_totals.csv")
    report = pd.read_csv(tmp_path / "data_quality_report.csv")

    assert len(yields) == 16
    assert len(daily) == 3
    assert len(report) == 8


def test_pipeline_daily_fat_matches_hand_calculation(tmp_path):
    """Cow 9001 on 2026-08-10, worked by hand from the example files.

    Milking 1: 36.9 lb = 16.7376 kg x 3.85% = 0.6444 kg of fat
    Milking 2: 35.2 lb = 15.9665 kg x 4.10% = 0.6546 kg of fat
    Milking 3: 32.8 lb = 14.8778 kg x 3.95% = 0.5877 kg of fat
    Daily total: 1.8867 kg of fat
    """
    run_pipeline("data/example", str(tmp_path))

    daily = pd.read_csv(tmp_path / "daily_totals.csv")
    is_cow = daily["Cow_ID"] == 9001
    is_day = daily["Milking_Date"] == "2026-08-10"

    assert daily[is_cow & is_day]["Fat_kg"].iloc[0] == 1.8867
