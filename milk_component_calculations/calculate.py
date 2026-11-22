"""Calculate milk-component yields.

Yield (kg) = milk (kg) x component percent / 100
"""

LB_TO_KG = 0.45359237

YIELD_COLUMNS = ["Milk_kg", "Fat_kg", "Protein_kg", "Lactose_kg"]


def lb_to_kg(pounds):
    """Convert pounds to kilograms."""
    return pounds * LB_TO_KG


def calculate_component_yields(merged_df, milk_unit="lb"):
    """Add milk (kg) and fat, protein, and lactose yield (kg) for each milking.

    milk_unit says how the "Milk" column was recorded: "lb" or "kg".
    """
    df = merged_df.copy()

    if milk_unit == "lb":
        df["Milk_kg"] = lb_to_kg(df["Milk"])
    elif milk_unit == "kg":
        df["Milk_kg"] = df["Milk"]
    else:
        raise ValueError(f'milk_unit must be "lb" or "kg", not "{milk_unit}"')

    df["Fat_kg"] = df["Milk_kg"] * df["Fat_Pct"] / 100
    df["Protein_kg"] = df["Milk_kg"] * df["Pro_Pct"] / 100
    df["Lactose_kg"] = df["Milk_kg"] * df["Lactose_Pct"] / 100

    return df


def calculate_daily_totals(yields_df, milkings_per_day=3):
    """Add up the yields of each cow for each day.

    A daily total is only correct when every milking of the day was sampled.
    Days with fewer complete milkings are left out of the totals.
    Returns the daily totals and the partially sampled days.
    """
    df = yields_df.copy()

    # A milking is complete when all three component yields are available
    df["Complete"] = df[["Fat_kg", "Protein_kg", "Lactose_kg"]].notna().all(axis=1)

    groups = df.groupby(["Cow_ID", "Milking_Date"])
    daily = groups[YIELD_COLUMNS].sum()
    daily["Milkings_Sampled"] = groups["Complete"].sum()
    daily = daily.reset_index()

    is_full_day = daily["Milkings_Sampled"] == milkings_per_day
    full_days = daily[is_full_day].copy()

    problems = daily[~is_full_day][["Cow_ID", "Milking_Date"]].copy()
    sampled = daily[~is_full_day]["Milkings_Sampled"].astype(str)
    problems["Problem"] = (
        "Only "
        + sampled
        + f" of {milkings_per_day} milkings sampled, day left out of daily totals"
    )

    print("Cow-days with every milking sampled:", len(full_days), "of", len(daily))
    return full_days, problems
