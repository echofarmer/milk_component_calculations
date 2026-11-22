"""Tests for the yield calculations, checked against values worked by hand."""

import pandas as pd

from milk_component_calculations.calculate import (
    calculate_component_yields,
    calculate_daily_totals,
    lb_to_kg,
)


def test_lb_to_kg():
    """100 lb is 45.3592 kg."""
    assert round(lb_to_kg(100), 4) == 45.3592


def test_yields_match_hand_calculation():
    """36.9 lb of milk with 3.85% fat, 3.12% protein, and 4.90% lactose.

    By hand:
    36.9 lb x 0.45359237 = 16.7376 kg of milk
    16.7376 x 3.85 / 100 = 0.6444 kg of fat
    16.7376 x 3.12 / 100 = 0.5222 kg of protein
    16.7376 x 4.90 / 100 = 0.8201 kg of lactose
    """
    merged = pd.DataFrame(
        {"Milk": [36.9], "Fat_Pct": [3.85], "Pro_Pct": [3.12], "Lactose_Pct": [4.90]}
    )

    result = calculate_component_yields(merged)

    assert round(result["Milk_kg"].iloc[0], 4) == 16.7376
    assert round(result["Fat_kg"].iloc[0], 4) == 0.6444
    assert round(result["Protein_kg"].iloc[0], 4) == 0.5222
    assert round(result["Lactose_kg"].iloc[0], 4) == 0.8201


def test_milk_in_kg_is_not_converted():
    """With milk_unit="kg", 30 kg of milk at 4% fat gives 1.2 kg of fat."""
    merged = pd.DataFrame(
        {"Milk": [30.0], "Fat_Pct": [4.0], "Pro_Pct": [3.0], "Lactose_Pct": [5.0]}
    )

    result = calculate_component_yields(merged, milk_unit="kg")

    assert result["Milk_kg"].iloc[0] == 30.0
    assert round(result["Fat_kg"].iloc[0], 4) == 1.2


def test_unknown_unit_stops_with_error():
    """A unit other than "lb" or "kg" is refused instead of guessed."""
    merged = pd.DataFrame(
        {"Milk": [30.0], "Fat_Pct": [4.0], "Pro_Pct": [3.0], "Lactose_Pct": [5.0]}
    )

    error_message = ""
    try:
        calculate_component_yields(merged, milk_unit="gallons")
    except ValueError as error:
        error_message = str(error)

    assert "milk_unit" in error_message


def test_missing_percent_gives_missing_yield():
    """A missing fat percentage gives a missing fat yield, not 0."""
    merged = pd.DataFrame(
        {"Milk": [30.0], "Fat_Pct": [None], "Pro_Pct": [3.0], "Lactose_Pct": [5.0]}
    )

    result = calculate_component_yields(merged)

    assert pd.isna(result["Fat_kg"].iloc[0])
    assert pd.notna(result["Protein_kg"].iloc[0])


def test_daily_totals_keep_only_fully_sampled_days():
    """Day 1 has 3 complete milkings; day 2 has 2; day 3 has a missing fat yield."""
    yields = pd.DataFrame(
        {
            "Cow_ID": [1, 1, 1, 1, 1, 1, 1, 1],
            "Milking_Date": ["d1", "d1", "d1", "d2", "d2", "d3", "d3", "d3"],
            "Milk_kg": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
            "Fat_kg": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, None, 0.4],
            "Protein_kg": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            "Lactose_kg": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        }
    )

    daily, partial_days = calculate_daily_totals(yields)

    assert len(daily) == 1
    assert daily["Milking_Date"].iloc[0] == "d1"
    assert round(daily["Fat_kg"].iloc[0], 4) == 1.2
    assert len(partial_days) == 2
