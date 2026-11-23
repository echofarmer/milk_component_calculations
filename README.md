# Milk Component Calculations

A Python package that combines milk-component lab results with milk-yield records and calculates fat, protein, and lactose yields for each cow.

## Project Purpose

Dairy farms and researchers collect milk data from more than one system. Milking-parlor software records how much milk each cow gives at each milking. A laboratory reports the fat, protein, and lactose percentages of milk samples taken at some of those milkings. To know how many kilograms of fat a cow produced, the two sources must be matched by cow, date, and milking, and checked for missing, duplicated, and implausible records.

Doing this by hand in spreadsheets is slow and hard to repeat. This project does it with one command, gives the same result every time, and lists every record that was changed or left out.

## What the Software Does

1. Loads Central Star component files (`.xlsx`) and BoviSync milk-yield files (`.csv`).
2. Checks data quality (see [Data-quality checks](#data-quality-checks)).
3. Matches the two sources by cow, date, and milking.
4. Calculates milk (kg) and fat, protein, and lactose yield (kg) for each milking:
   `yield (kg) = milk (kg) x component % / 100`
5. Calculates daily totals for the days on which every milking was sampled, and the mean daily yield of each cow.
6. Saves four tables and one chart.

## Quick Start

Requirements: [Anaconda or Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) and Git. Everything else (Python, pandas, pytest, Ruff, pdoc, and `make`) is installed by the conda environment.

```
git clone https://github.com/echofarmer/milk_component_calculations.git
cd milk_component_calculations
conda env create -f environment.yml
conda activate milk_component_calculations
make run
```

`make run` runs the full workflow on the invented example files in `data/example/` and saves the results in a new `outputs/` folder. No real data are needed.

If `make` is already installed on your computer, `make init` creates the same environment.

## Expected Output

`make run` prints one line for each step:

```
--- 1. Load the files ---
Number of component files found:  1
data/example/milk/9001.csv: removed 3 summary rows
data/example/milk/9002.csv: removed 3 summary rows
data/example/milk/9003.csv: removed 3 summary rows

--- 2. Check the component records ---
Component records with a 0 value: 1
Component records outside the expected range: 0

--- 3. Check the milk records ---
Milk records on dates without samples, not used: 0
Duplicate milking records removed: 1
Records with unknown milking number removed: 1

--- 4. Match the two sources ---
Records added together within a milking: 0
Matched milkings: 16
Records found in only one source: 2

--- 5. Calculate the yields ---
Cow-days with every milking sampled: 3 of 6

--- 6. Save the results ---
Milkings with yields: 16
Fully sampled cow-days: 3
Rows in the data-quality report: 8
Results saved in: outputs
```

It saves these files in `outputs/`:

| File | Contents |
|---|---|
| `yields_per_milking.csv` | One row per matched milking: component percentages, milk, and fat, protein, and lactose yield (kg) |
| `daily_totals.csv` | Daily yield of each cow, only for fully sampled days |
| `summary_by_cow.csv` | Mean daily yield of each cow |
| `data_quality_report.csv` | Every record that was changed, removed, or not used, with the reason |
| `daily_yields_by_cow.png` | Bar chart of the mean daily yields |

`daily_totals.csv` for the example data:

| Cow_ID | Milking_Date | Milk_kg | Fat_kg | Protein_kg | Lactose_kg | Milkings_Sampled |
|---|---|---|---|---|---|---|
| 9001 | 2026-08-10 | 47.5818 | 1.8867 | 1.4864 | 2.3298 | 3 |
| 9001 | 2026-08-11 | 47.7179 | 1.8972 | 1.4971 | 2.3317 | 3 |
| 9002 | 2026-08-11 | 40.9140 | 1.8069 | 1.3476 | 1.9734 | 3 |

`data_quality_report.csv` for the example data:

| Cow_ID | Milking_Date | Milking_Time | Problem |
|---|---|---|---|
| 9002 | 2026-08-10 | 2 | Component value of 0 (failed sample), set to missing |
| 9002 | 2026-08-10 | 2 | Exact duplicate milking record, removed |
| 9003 | 2026-08-10 | | Unreadable milking time, milking number unknown, removed |
| 9003 | 2026-08-10 | 2 | Component record with no matching milk record, not used |
| 9003 | 2026-08-11 | 2 | Milk record with no matching component record, not used |
| 9002 | 2026-08-10 | | Only 2 of 3 milkings sampled, day left out of daily totals |
| 9003 | 2026-08-10 | | Only 2 of 3 milkings sampled, day left out of daily totals |
| 9003 | 2026-08-11 | | Only 2 of 3 milkings sampled, day left out of daily totals |

## Commands

Run these from the repository root, with the environment active.

| Command | What it does |
|---|---|
| `make help` | List all available commands |
| `make init` | Create or update the conda environment |
| `make run` | Run the full workflow on the example data |
| `make test` | Run the automated tests with pytest |
| `make lint` | Check code style and common errors with Ruff |
| `make format` | Format the code with Ruff |
| `make check` | Run the lint and the tests |
| `make docs` | Build the documentation with pdoc in `docs/` |
| `make clean` | Remove generated files (`outputs/`, `docs/`, caches) |

## Data-Quality Checks

| Check | What the software does |
|---|---|
| Summary rows in the milk files (`month`, `daily`) | Dropped when loading |
| Milk record from a date with no component samples | Not used |
| Component value of 0 | Set to missing, because 0 means a failed sample |
| Fat, protein, or lactose outside the expected range | Reported and kept |
| Exact duplicate milking record | Removed |
| Unreadable milking time | Record removed, because its milking number is unknown |
| More than one record in the same milking | Milk added together |
| Record found in only one source | Not used |
| Day with fewer than 3 sampled milkings | Left out of the daily totals |

The first two cases are counted in the printed output. Every other case is listed record by record in `data_quality_report.csv`, so no record disappears silently.

## Assumptions and Limitations

- **Units.** Milk in the BoviSync files is read as pounds and converted to kilograms (1 lb = 0.45359237 kg). For files in kilograms, use `milk_unit="kg"`.
- **Milking number.** The milk files give a clock time. The milking number is assigned from it: before 11:00 is milking 1, 11:00 to 17:59 is milking 2, and 18:00 or later is milking 3. A herd with other milking times needs other cut-offs. A milking recorded after midnight would be counted as milking 1 of the next date.
- **Three milkings per day.** Daily totals are reported only when all 3 milkings of the day have component results. Other days would be underestimated, so they are left out and reported.
- **Component file layout.** The loader expects the Central Star layout: 4 header rows, then 9 columns in a fixed order. A file with another layout would be read incorrectly.
- **Expected ranges.** The default ranges are wide (fat 1 to 9%, protein 1.5 to 6%, lactose 3 to 6%). Values outside them are reported, not removed.
- **Other columns.** Solids, SCC, and MUN are kept in the output but are not used in any calculation.
- **Validation so far.** The tests use invented example data and values calculated by hand. The results have not yet been compared with the original analysis of the real trial data.

## Using Your Own Data

Put the files in one folder with two subfolders:

```
my_data/
    components/    Central Star .xlsx files
    milk/          BoviSync .csv files, one per cow
```

Then give the data folder and an output folder to the workflow:

```
python -m milk_component_calculations.pipeline path/to/my_data path/to/my_outputs
```

The functions can also be used from Python (run `pip install -e .` once so the package can be imported from any folder):

```python
from milk_component_calculations.pipeline import run_pipeline

yields = run_pipeline("path/to/my_data", "path/to/my_outputs", milk_unit="lb")
```

Real trial data should stay outside the repository. The folders `data/raw/` and `outputs/` are ignored by Git.

## Tests

`make test` runs 22 tests. All of them should end with `PASSED`.

- **Loading:** the first cow is not lost as a header, summary rows are dropped, an unreadable time is not guessed, an empty folder gives a clear error, and two date formats are read.
- **Data-quality checks:** each problem planted in `data/example/` is found by its check (see `data/example/README.md`).
- **Calculations:** yields match values worked by hand. For example, 36.9 lb of milk at 3.85% fat is 16.7376 kg of milk and 0.6444 kg of fat.
- **Full workflow:** the example data give 16 matched milkings, 3 fully sampled cow-days, and 8 rows in the data-quality report.

The same lint, tests, and example workflow run on GitHub for every push (`.github/workflows/ci.yml`).

## Documentation

`make docs` builds the documentation of every module and function in `docs/`. Open `docs/index.html` in a browser to read it.

## Repository Layout

```
milk_component_calculations/
    uploading.py     read the Central Star and BoviSync files
    validate.py      data-quality checks
    merge.py         combine milkings and match the two sources
    calculate.py     unit conversion, component yields, daily totals
    pipeline.py      run the full workflow and save the results
    tests/           automated tests
data/example/        invented example files with planted problems
paper/               proposal, final paper, and course notes
environment.yml      conda environment
makefile             project commands
```

## AI Assistance

Claude (Anthropic) helped write the data-quality, matching, and calculation.
## License

MIT. See `LICENSE`.
