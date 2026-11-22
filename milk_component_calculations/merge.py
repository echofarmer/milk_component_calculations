"""Combine repeated milkings and match the two data sources."""

import numpy as np

# A component record and a milk record belong together when these three match
MATCH_COLUMNS = ["Cow_ID", "Milking_Date", "Milking_Time"]


def combine_milkings(milk_df):
    """Add up the milk of records from the same cow, date, and milking.

    A cow can have two records in one milking, for example when the milking
    unit is attached a second time. Their milk is added together so that
    every milking has one row.
    Returns the combined dataframe and the records that were added together.
    """
    df = milk_df.copy()

    # True for every record that shares its cow, date, and milking with another
    is_repeated = df.duplicated(subset=MATCH_COLUMNS, keep=False)

    problems = df[is_repeated].copy()
    problems["Problem"] = "More than one record in the milking, milk added together"

    combined = df.groupby(MATCH_COLUMNS, as_index=False)["Milk"].sum()

    print("Records added together within a milking:", is_repeated.sum())
    return combined, problems


def merge_sources(components_df, milk_df):
    """Match component records to milk records by cow, date, and milking.

    Returns the matched rows and the records found in only one source.
    """
    # how="outer" keeps every record; the "_merge" column says where it was found
    both = components_df.merge(milk_df, on=MATCH_COLUMNS, how="outer", indicator=True)

    merged = both[both["_merge"] == "both"].drop(columns="_merge")

    unmatched = both[both["_merge"] != "both"].copy()
    unmatched["Problem"] = np.where(
        unmatched["_merge"] == "left_only",
        "Component record with no matching milk record, not used",
        "Milk record with no matching component record, not used",
    )
    unmatched = unmatched.drop(columns="_merge")

    print("Matched milkings:", len(merged))
    print("Records found in only one source:", len(unmatched))
    return merged, unmatched
