"""Data-quality checks for the milk-component and milk-yield tables.

Every check returns two tables:

1. the data after the check
2. the problem rows, with a "Problem" column that says what was found

The pipeline joins the problem rows from every check into one data-quality
report, so no record is changed or removed without being listed.
"""

import numpy as np
import pandas as pd

COMPONENT_COLUMNS = [
    "Fat_Pct",
    "Pro_Pct",
    "Lactose_Pct",
    "Solids_Pct",
    "SCC_1000_ml",
    "MUN_mg_dl",
]

# Expected range (lowest, highest) of each component, in percent.
# Values outside the range are reported but kept in the data.
DEFAULT_LIMITS = {
    "Fat_Pct": (1.0, 9.0),
    "Pro_Pct": (1.5, 6.0),
    "Lactose_Pct": (3.0, 6.0),
}


def check_failed_samples(components_df):
    """Set component values of 0 to missing.

    A value of 0 means the lab sample failed or was not analyzed. It is not a
    real measurement, so it must not be used in the calculations.
    Returns the cleaned dataframe and the rows that had a 0.
    """
    df = components_df.copy()

    # True for every row where at least one component is 0
    has_zero = (df[COMPONENT_COLUMNS] == 0).any(axis=1)

    problems = df[has_zero].copy()
    problems["Problem"] = "Component value of 0 (failed sample), set to missing"

    df[COMPONENT_COLUMNS] = df[COMPONENT_COLUMNS].replace(0, np.nan)

    print("Component records with a 0 value:", has_zero.sum())
    return df, problems


def check_component_ranges(components_df, limits=None):
    """Report fat, protein, or lactose values outside the expected range.

    Nothing is removed, because an unusual value can still be real.
    limits is a dictionary such as {"Fat_Pct": (1.0, 9.0)}. If it is not
    given, DEFAULT_LIMITS is used.
    Returns the unchanged dataframe and the rows with a value out of range.
    """
    if limits is None:
        limits = DEFAULT_LIMITS

    df = components_df.copy()

    # Start with False for every row, then mark rows with a value out of range
    is_outside = pd.Series(False, index=df.index)
    for column in limits:
        lowest = limits[column][0]
        highest = limits[column][1]
        is_outside = is_outside | (df[column] < lowest) | (df[column] > highest)

    problems = df[is_outside].copy()
    problems["Problem"] = "Component value outside the expected range, kept"

    print("Component records outside the expected range:", is_outside.sum())
    return df, problems


def check_duplicate_milkings(milk_df):
    """Remove milking records that are exact copies of another record.

    Returns the cleaned dataframe and the copies that were removed.
    """
    df = milk_df.copy()

    # True for the second (and later) copy of an identical row
    is_duplicate = df.duplicated()

    problems = df[is_duplicate].copy()
    problems["Problem"] = "Exact duplicate milking record, removed"

    df = df[~is_duplicate].copy()

    print("Duplicate milking records removed:", is_duplicate.sum())
    return df, problems


def check_unknown_milking(milk_df):
    """Remove milking records whose milking number could not be read.

    Without the milking number, the record cannot be matched to a lab sample.
    Returns the cleaned dataframe and the records that were removed.
    """
    df = milk_df.copy()

    is_unknown = df["Milking_Time"].isna()

    problems = df[is_unknown].copy()
    problems["Problem"] = "Unreadable milking time, milking number unknown, removed"

    df = df[~is_unknown].copy()

    print("Records with unknown milking number removed:", is_unknown.sum())
    return df, problems
