"""Tests for loading the example Central Star and BoviSync files."""

from milk_component_calculations.uploading import (
    clean_milk_yield_files,
    load_milk_components,
)


def test_components_keeps_first_cow():
    """All 17 example records load, starting with cow 9001 (header=None bug)."""
    df = load_milk_components("data/example/components")
    assert len(df) == 17
    assert df["Cow_ID"].iloc[0] == 9001


def test_milk_drops_summary_rows():
    """Only the 19 milking records remain after dropping summary rows."""
    df = clean_milk_yield_files("data/example/milk")
    assert len(df) == 19


def test_unreadable_time_is_missing():
    """The '??:??' milking gets a missing milking number, not 3."""
    df = clean_milk_yield_files("data/example/milk")
    assert df["Milking_Time"].isna().sum() == 1
    