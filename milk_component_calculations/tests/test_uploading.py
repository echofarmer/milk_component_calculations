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


def test_empty_folder_gives_clear_error(tmp_path):
    """A folder with no files stops the program with a clear message."""
    error_message = ""
    try:
        load_milk_components(str(tmp_path))
    except FileNotFoundError as error:
        error_message = str(error)

    assert "No .xlsx files found" in error_message


def test_dates_in_two_formats_are_read(tmp_path):
    """One file writes 2026-08-12 and another 8/12/2026; both are the same day."""
    header = "Date,Time,Animal,Milk\n"
    (tmp_path / "9001.csv").write_text(header + "2026-08-12,03:40,9001,36.9\n")
    (tmp_path / "9002.csv").write_text(header + "8/12/2026,03:44,9002,31.2\n")

    df = clean_milk_yield_files(str(tmp_path))

    assert len(df) == 2
    assert df["Milking_Date"].nunique() == 1
