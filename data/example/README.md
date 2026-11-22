# Example data

These files are invented. They contain no real animals or trial records.
They copy the layout of the real exports so the code can be demonstrated and
tested without publishing research data.

## Files

| Folder | Format | Mimics |
|---|---|---|
| `components/` | Excel (`.xlsx`), 4 header rows, then one row per cow per milking | Central Star milk-component report |
| `milk/` | CSV, one file per cow, with `month` and `daily` summary rows mixed in | BoviSync milk-yield export |

Cows: 9001, 9002, 9003. Dates: 2026-08-10 and 2026-08-11. Milkings: 1, 2, 3.
Milk is in pounds, as in the BoviSync export.

## Planted data-quality problems

Each problem is included on purpose so the code's checks can be verified.

| Case | Where | Expected behavior |
|---|---|---|
| First data row is a real record | `components/`, row 5 (cow 9001) | Loaded, not treated as a header |
| Failed sample (all components 0) | `components/`, cow 9002, 2026-08-10, milking 2 | Zeros converted to missing values and reported |
| Missing milking sample | `components/`, cow 9003, 2026-08-11, milking 2 absent | Milk record reported as unmatched, and the day reported as partially sampled |
| Summary rows | every `milk/*.csv` (`month`, `daily`) | Dropped when loading |
| Duplicated milking record | `milk/9002.csv`, 2026-08-10, 11:52 | Copy removed and reported |
| Unreadable milking time | `milk/9003.csv`, 2026-08-10, `??:??` | Milking number left missing, not guessed; record removed and reported |

## Expected counts

- Component records: 17 (3 cows × 2 days × 3 milkings, minus 1)
- Milking records after dropping summary rows: 19 (18 + 1 duplicate)
- Milking records after removing the duplicate and the unreadable record: 17
- Matched milkings: 16
- Fully sampled cow-days: 3 of 6 (cow 9001 on both days, cow 9002 on 2026-08-11)
- Rows in the data-quality report: 8
