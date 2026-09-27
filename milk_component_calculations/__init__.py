"""Merge dairy milk-component and milk-yield records and calculate component yields.

Inputs:
- Central Star Excel exports: fat, protein, and lactose percentages per cow
  per milking.
- BoviSync CSV exports: milk yield per cow per milking.

Workflow:
1. Load both sources and standardize column names and data types.
2. Clean data: clean missing data and identify duplicated records.
3. Combine repeated BoviSync records within a milking, then match the two
   sources by cow, date, and milking.
4. Calculate fat, protein, and lactose yield (kg) for each milking.
5. Export a cleaned and merged dataset with calculated component yields.

Modules:
- ``load``: read Central Star and BoviSync files
- ``validate``: data-quality checks and flags
- ``merge``: combine milkings, match sources, filter by date
- ``calculate``: component yields and unit conversion
- ``pipeline``: run the full workflow and export results
"""



# ---------------------------------------------------------------------------
# Scaffold examples for future package growth
# ---------------------------------------------------------------------------
# 1) Grouped imports from multiple modules:
# Learn more: https://realpython.com/python-modules-packages/
# from milk_component_calculations.algebra import solve_linear
# from milk_component_calculations.stats import mean_center
# __all__.extend(["solve_linear", "mean_center"])

# 2) Re-export everything from selected submodules using a loop:
# Learn more: https://docs.python.org/3/reference/import.html
# from milk_component_calculations import algebra as _algebra
# from milk_component_calculations import stats as _stats
#
# for _module in (_algebra, _stats):
#     __all__.extend(getattr(_module, "__all__", []))

# 3) Optional lazy imports for heavy dependencies:
# Learn more: https://peps.python.org/pep-0562/
# def __getattr__(name: str):
#     if name == "slow_model":
#         from milk_component_calculations.models import slow_model
#         return slow_model
#     raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
