# Milk Component Calculations

A Python software project for cleaning raw dairy-production data and calculating milk fat, protein, and lactose yields.

## Project Purpose

Dairy-production datasets often contain milk yield and milk-component percentages, but the raw records may include missing values, duplicated observations, incorrect formats, or inconsistent units. This project will develop a reproducible Python workflow for checking these data and calculating milk-component yields.

The software is intended to make dairy-data analysis more accurate, efficient, and reproducible than performing repeated calculations manually in spreadsheets.

## Main Functionality

The software will:

1. Import raw dairy-production data from a CSV file.
2. Verify that required columns are present.
3. identify missing values and duplicated records.
4. Flag values outside user-defined acceptable ranges.
5. Calculate fat, protein, and lactose yields.
6. Create basic tables.
7. Export a clean CSV file.

## How to get started

### Requirements

- Anaconda
- All other tools (Python, pandas, pytest, Ruff, and `make` on Windows) are installed by the conda environment 

### 1. Download the repository

```
git clone https://github.com/echofarmer/milk_component_calculations.git
cd milk_component_calculations
```

### 2. Create the environment and install the package
```
Make init
conda activate milk_component_calculations
pip install -e .
```

## 3. Run the example workflow
```
python milk_component_calculations/uploading.py
```

This loads the invented example files in `data/example/` and prints the results. Expected output includes:

- 17 component records, starting with cow 9001
- 3 summary rows removed from each milk-yield file
- `Rows kept: 10` after filtering to 2026-08-10
  
### 4. Run the checks

| Command | What it does |
|---|---|
| `make help` | List all available commands |
| `make lint` | Check code style and common errors with Ruff |
| `make format` | Automatically format the code with Ruff |
| `make test` | Run the automated tests with pytest |


### Using your own data

The loaders take a folder path, so your data can stay outside the repository:

```python
from milk_component_calculations.uploading import (
    clean_milk_yield_files,
    load_milk_components,
)

components = load_milk_components("path/to/central_star_files")
milk = clean_milk_yield_files("path/to/bovisync_files")
```

Expected input formats:

- **Milk components:** Central Star Excel exports (`.xlsx`) with 4 header rows.
- **Milk yield:** BoviSync CSV exports, one file per cow.

