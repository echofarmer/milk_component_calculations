"""Tests for combining repeated milkings and matching the two sources."""

import pandas as pd

from milk_component_calculations.merge import combine_milkings, merge_sources
from milk_component_calculations.uploading import (
    clean_milk_yield_files,
    load_milk_components,
)
from milk_component_calculations.validate import (
    check_duplicate_milkings,
    check_unknown_milking,
)


def test_repeated_records_are_added_together():
    """Two records in milking 1 (10 + 5) become one row with 15."""
    milk = pd.DataFrame(
        {
            "Cow_ID": [1, 1, 1],
            "Milking_Date": ["2026-08-10", "2026-08-10", "2026-08-10"],
            "Milking_Time": [1, 1, 2],
            "Milk": [10.0, 5.0, 12.0],
        }
    )

    combined, problems = combine_milkings(milk)

    assert len(combined) == 2
    assert combined["Milk"].tolist() == [15.0, 12.0]
    assert len(problems) == 2


def test_example_sources_match_on_16_milkings():
    """17 component records and 17 clean milk records share 16 milkings.

    Not matched: the component record of cow 9003 on 2026-08-10, milking 2
    (its milk record has an unreadable time), and the milk record of cow 9003
    on 2026-08-11, milking 2 (no sample was taken).
    """
    components = load_milk_components("data/example/components")
    milk = clean_milk_yield_files("data/example/milk")
    milk, duplicates = check_duplicate_milkings(milk)
    milk, unknown = check_unknown_milking(milk)
    milk, repeated = combine_milkings(milk)

    merged, unmatched = merge_sources(components, milk)

    assert len(merged) == 16
    assert len(unmatched) == 2
    assert unmatched["Cow_ID"].tolist() == [9003, 9003]
