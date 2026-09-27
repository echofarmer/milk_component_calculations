
import glob

import numpy as np
import pandas as pd


def load_milk_components(folder_name="Milk_Comp"):
    """
    Finds all Excel files in the specified folder, extracts the component data,
    cleans the data types, and returns a single combined dataframe.
    """
    search_pattern = f"{folder_name}/*.xlsx"
    files_available = sorted(glob.glob(search_pattern))

    print("Number of component files found: ", len(files_available))

    clean_columns = [
        "Cow_ID",
        "Milking_Date",
        "Milking_Time",
        "Fat_Pct",
        "Pro_Pct",
        "Lactose_Pct",
        "Solids_Pct",
        "SCC_1000_ml",
        "MUN_mg_dl",
    ]

    all_dataframes = []

    for file in files_available:
        df = pd.read_excel(file, skiprows=4, header=None, names=clean_columns)
        df["Source_File"] = file
        all_dataframes.append(df)

    master_df = pd.concat(all_dataframes, ignore_index=True)
    master_df["Cow_ID"] = master_df["Cow_ID"].astype("Int64")
    master_df["Milking_Date"] = pd.to_datetime(master_df["Milking_Date"]).dt.date

    return master_df


def clean_milk_yield_files(input_folder="Milk"):
    """
    Iterates through raw CSV files, cleans the data, calculates the shift,
    and combines ALL files into one single dataframe.
    """
    files = sorted(glob.glob(f"{input_folder}/*.csv"))
    processed_dataframes = []

    for file in files:
        df = pd.read_csv(file)

        # Filter the Animal and Milk columns
        df["Animal"] = pd.to_numeric(df["Animal"], errors="coerce")
        df["Milk"] = pd.to_numeric(df["Milk"], errors="coerce")
        rows_before = len(df)
        df = df.dropna(subset=["Animal", "Milk"]).copy()
        print(f"{file}: removed {rows_before - len(df)} summary rows")

        # Create the 'Milking' column based on the Time column
        temp_time = pd.to_datetime(df["Time"], format="%H:%M", errors="coerce")
        conditions = [
            (temp_time.dt.hour < 11),
            (temp_time.dt.hour >= 11) & (temp_time.dt.hour < 18),
        ]
        choices = [1, 2]
        df["Milking"] = np.select(conditions, choices, default=3)

        df["Milking"] = df["Milking"].astype("Int64")
        df.loc[temp_time.isna(), "Milking"] = pd.NA

        # Delete unneeded columns
        cols_to_drop = [
            "Conductivity",
            "Duration",
            "Peak flow",
            "Shift date",
            "Shift",
            "Period",
        ]
        df = df.drop(columns=cols_to_drop, errors="ignore")

        # Clean up Cow ID
        df["Animal"] = df["Animal"].astype("Int64")

        # Add the clean dataframe to our list
        processed_dataframes.append(df)

    # Combine all individual cow dataframes into one master dataset
    combined_df = pd.concat(processed_dataframes, ignore_index=True)

    combined_df = combined_df.rename(
        columns={"Animal": "Cow_ID", "Date": "Milking_Date", "Milking": "Milking_Time"}
    )
    combined_df["Milking_Date"] = pd.to_datetime(combined_df["Milking_Date"]).dt.date

    return combined_df


def filter_milk_yield_dates(df, dates_to_keep=None):
    """
    Filters the milk yield dataframe to keep only specific dates.
    """
    if dates_to_keep is None:
        dates_to_keep = [
            "2026-07-13",
            "2026-07-20",
            "2026-07-27",
            "2026-08-03",
            "2026-08-04",
            "2026-08-05",
            "2026-08-06",
            "2026-08-07",
        ]

    target_dates = pd.to_datetime(dates_to_keep).date

    # Filter the dataset
    filtered_df = df[df["Milking_Date"].isin(target_dates)].copy()

    return filtered_df


if __name__ == "__main__":
    print("--- Loading Milk Components ---")
    master_components_df = load_milk_components("data/example/components")
    print(master_components_df.head())

    print("\n--- Cleaning & Combining Milk Yield Files ---")
    combined_yield_df = clean_milk_yield_files("data/example/milk")
    print(combined_yield_df.head())

    print("\n--- Filtering Combined Milk Yield Dates ---")
    final_yield_df = filter_milk_yield_dates(combined_yield_df, ["2026-08-10"])
    print("Rows kept:", len(final_yield_df))