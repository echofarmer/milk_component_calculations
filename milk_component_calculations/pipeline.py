"""Run the full workflow: load, check, match, calculate, and save.

Run it from the repository root with the example data:

    python -m milk_component_calculations.pipeline

or with your own folders:

    python -m milk_component_calculations.pipeline path/to/data path/to/outputs

The data folder must have two subfolders: "components" (Central Star .xlsx
files) and "milk" (BoviSync .csv files). A third argument, "lb" or "kg", says
how the milk was recorded. The default is "lb".
"""

import os
import sys

import pandas as pd
from matplotlib.figure import Figure

from milk_component_calculations.calculate import (
    YIELD_COLUMNS,
    calculate_component_yields,
    calculate_daily_totals,
)
from milk_component_calculations.merge import (
    MATCH_COLUMNS,
    combine_milkings,
    merge_sources,
)
from milk_component_calculations.uploading import (
    clean_milk_yield_files,
    filter_milk_yield_dates,
    load_milk_components,
)
from milk_component_calculations.validate import (
    check_component_ranges,
    check_duplicate_milkings,
    check_failed_samples,
    check_unknown_milking,
)

REPORT_COLUMNS = ["Cow_ID", "Milking_Date", "Milking_Time", "Problem"]


def build_quality_report(problem_tables):
    """Join the problem rows from every check into one table."""
    parts = []
    for table in problem_tables:
        if len(table) > 0:
            # Keep the same four columns from every check
            parts.append(table.reindex(columns=REPORT_COLUMNS).astype(object))

    if len(parts) == 0:
        return pd.DataFrame(columns=REPORT_COLUMNS)

    return pd.concat(parts, ignore_index=True)


def save_yield_chart(daily, file_name):
    """Save a bar chart of the mean daily component yield of each cow."""
    cow_means = daily.groupby("Cow_ID")[["Fat_kg", "Protein_kg", "Lactose_kg"]].mean()
    cow_means.columns = ["Fat", "Protein", "Lactose"]

    # A Figure made this way is only saved to a file; it never opens a window
    figure = Figure(figsize=(7, 4))
    axes = figure.subplots()

    cow_means.plot(kind="bar", ax=axes, rot=0)
    axes.set_ylim(0, cow_means.max().max() * 1.25)  # leave room for the legend
    axes.legend(loc="upper center", ncol=3)
    axes.set_xlabel("Cow")
    axes.set_ylabel("Mean daily yield (kg)")
    axes.set_title("Mean daily component yield per cow")
    figure.tight_layout()
    figure.savefig(file_name, dpi=150)


def run_pipeline(data_folder="data/example", output_folder="outputs", milk_unit="lb"):
    """Run every step and save the results. Returns the yields per milking."""
    print("--- 1. Load the files ---")
    components = load_milk_components(f"{data_folder}/components")
    milk = clean_milk_yield_files(f"{data_folder}/milk")

    print("\n--- 2. Check the component records ---")
    components, failed_samples = check_failed_samples(components)
    components, out_of_range = check_component_ranges(components)

    print("\n--- 3. Check the milk records ---")
    # Only milk from dates with component samples can be matched
    sampled_dates = components["Milking_Date"].unique()
    records_before = len(milk)
    milk = filter_milk_yield_dates(milk, sampled_dates)
    print(
        "Milk records on dates without samples, not used:", records_before - len(milk)
    )
    milk, duplicates = check_duplicate_milkings(milk)
    milk, unknown_milkings = check_unknown_milking(milk)

    print("\n--- 4. Match the two sources ---")
    milk, repeated = combine_milkings(milk)
    merged, unmatched = merge_sources(components, milk)

    print("\n--- 5. Calculate the yields ---")
    yields = calculate_component_yields(merged, milk_unit)
    yields = yields.sort_values(MATCH_COLUMNS)
    daily, partial_days = calculate_daily_totals(yields)

    # Mean daily yield of each cow, from the fully sampled days
    summary = daily.groupby("Cow_ID")[YIELD_COLUMNS].mean()
    summary["Days"] = daily.groupby("Cow_ID").size()
    summary = summary.reset_index()

    report = build_quality_report(
        [
            failed_samples,
            out_of_range,
            duplicates,
            unknown_milkings,
            repeated,
            unmatched,
            partial_days,
        ]
    )

    print("\n--- 6. Save the results ---")
    os.makedirs(output_folder, exist_ok=True)
    yields.round(4).to_csv(f"{output_folder}/yields_per_milking.csv", index=False)
    daily.round(4).to_csv(f"{output_folder}/daily_totals.csv", index=False)
    summary.round(4).to_csv(f"{output_folder}/summary_by_cow.csv", index=False)
    report.to_csv(f"{output_folder}/data_quality_report.csv", index=False)

    if len(daily) > 0:
        save_yield_chart(daily, f"{output_folder}/daily_yields_by_cow.png")
    else:
        print("No fully sampled days, so no chart was made.")

    print("Milkings with yields:", len(yields))
    print("Fully sampled cow-days:", len(daily))
    print("Rows in the data-quality report:", len(report))
    print("Results saved in:", output_folder)

    return yields


if __name__ == "__main__":
    # Optional arguments: data folder, output folder, milk unit
    data_folder = "data/example"
    output_folder = "outputs"
    milk_unit = "lb"

    if len(sys.argv) > 1:
        data_folder = sys.argv[1]
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
    if len(sys.argv) > 3:
        milk_unit = sys.argv[3]

    run_pipeline(data_folder, output_folder, milk_unit)
