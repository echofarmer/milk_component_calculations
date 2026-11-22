"""Tests for the data-quality checks, using the invented example files.

Each test targets one problem that was planted in data/example on purpose.
"""

from milk_component_calculations.uploading import (
    clean_milk_yield_files,
    load_milk_components,
)
from milk_component_calculations.validate import (
    check_component_ranges,
    check_duplicate_milkings,
    check_failed_samples,
    check_unknown_milking,
)


def test_failed_sample_is_reported_and_set_to_missing():
    """Cow 9002, 2026-08-10, milking 2 has all components = 0."""
    components = load_milk_components("data/example/components")
    clean, problems = check_failed_samples(components)

    assert len(problems) == 1
    assert problems["Cow_ID"].iloc[0] == 9002
    assert clean["Fat_Pct"].isna().sum() == 1
    assert (clean["Fat_Pct"] == 0).sum() == 0


def test_example_values_are_inside_the_expected_range():
    """After the failed sample is set to missing, no example value is unusual."""
    components = load_milk_components("data/example/components")
    components, failed = check_failed_samples(components)
    clean, problems = check_component_ranges(components)

    assert len(problems) == 0


def test_value_out_of_range_is_reported_and_kept():
    """A fat percentage of 12 is reported, and the record stays in the data."""
    components = load_milk_components("data/example/components")
    components, failed = check_failed_samples(components)
    components.loc[0, "Fat_Pct"] = 12.0

    clean, problems = check_component_ranges(components)

    assert len(problems) == 1
    assert len(clean) == len(components)


def test_duplicate_milking_is_removed():
    """Cow 9002 has one copied record at 11:52 on 2026-08-10."""
    milk = clean_milk_yield_files("data/example/milk")
    clean, problems = check_duplicate_milkings(milk)

    assert len(problems) == 1
    assert problems["Cow_ID"].iloc[0] == 9002
    assert len(clean) == 18


def test_unknown_milking_is_removed():
    """Cow 9003 has one record with the time '??:??'."""
    milk = clean_milk_yield_files("data/example/milk")
    clean, problems = check_unknown_milking(milk)

    assert len(problems) == 1
    assert problems["Cow_ID"].iloc[0] == 9003
    assert clean["Milking_Time"].isna().sum() == 0
