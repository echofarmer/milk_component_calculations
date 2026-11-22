"""Merge dairy milk-component and milk-yield records and calculate component yields.

Inputs:
- Central Star Excel exports: fat, protein, and lactose percentages per cow
  per milking.
- BoviSync CSV exports: milk yield per cow per milking.

Workflow:
1. Load both sources and standardize column names and data types.
2. Check data quality: failed samples, values out of range, duplicated
   records, and unreadable milking times.
3. Combine repeated BoviSync records within a milking, then match the two
   sources by cow, date, and milking.
4. Calculate fat, protein, and lactose yield (kg) for each milking, and daily
   totals for the days on which every milking was sampled.
5. Save the merged dataset, the summaries, a chart, and a data-quality report.

Modules:
- ``uploading``: read the Central Star and BoviSync files
- ``validate``: data-quality checks
- ``merge``: combine milkings and match the two sources
- ``calculate``: unit conversion, component yields, and daily totals
- ``pipeline``: run the full workflow and save the results
"""
