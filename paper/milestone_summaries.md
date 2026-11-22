# Milestone Summaries

Short summaries for Milestones 3 to 5, following the "Evidence of Completion" prompts on the course site.

Repository: <https://github.com/echofarmer/milk_component_calculations>

## Milestone 3: Testing and Validation Baseline

**What was tested or validated**

- Loading: the first data row of a component file is kept, summary rows in the milk files are dropped, an unreadable milking time is left missing, an empty folder gives a clear error, and two date formats are read.
- Data-quality checks: each problem planted in `data/example/` is found by its check (failed sample, duplicate record, unreadable milking time, value out of range).
- Calculations: yields match values worked by hand. For example, 36.9 lb of milk at 3.85% fat is 16.7376 kg of milk and 0.6444 kg of fat. A missing percentage gives a missing yield, and an unknown unit is refused.
- Full workflow: the example data give 16 matched milkings, 3 fully sampled cow-days, and 8 rows in the data-quality report.

**Tool or workflow used**

pytest, run with `make test` (22 tests). `make check` runs Ruff and the tests. GitHub Actions runs the lint, the tests, and the example workflow on every push.

**What remains untested or still needs attention**

- The results have not yet been compared with the original analysis of the real trial data.
- The milking number is assigned from the clock time. Milkings after midnight and herds with other milking times are not handled.
- A component file with a layout other than the Central Star export is not detected.

**How the validation supports the final report**

The hand-calculated tests are the evidence that the yields are correct. The planted problems and the data-quality report are the evidence that no record is changed or removed silently. The assumptions and limitations are listed in the README and will be carried into the paper.

## Milestone 4: Documentation and Reproducibility Pass

**What documentation or reproducibility improvements were added**

- The README now has the project purpose, a quick start, the expected output with example tables, the commands, the data-quality checks, the assumptions and limitations, and instructions for other data.
- Every module and function has a docstring. `make docs` builds the documentation with pdoc.
- `data/example/README.md` lists the example files, the planted problems, and the expected counts.

**Tool or workflow used**

A conda environment (`environment.yml`), the Makefile, and pdoc.

**How a reviewer should run or evaluate the project**

```
git clone https://github.com/echofarmer/milk_component_calculations.git
cd milk_component_calculations
conda env create -f environment.yml
conda activate milk_component_calculations
make check
make run
```

`make check` should end with `22 passed`. The counts printed by `make run` and the files in `outputs/` should match the "Expected Output" section of the README.

**How these materials support the JOSS-style manuscript**

The purpose and limitations sections of the README are the starting point for the statement of need and the limitations in `paper/paper.md`. The example data let a reader reproduce the reported numbers without access to the trial data.

## Milestone 5: Project Systems and Automation

**Which project workflow was automated**

The whole analysis, from the export files to the result tables and the chart, runs with one command from the repository root.

**Command or tool used**

`make run`, a Makefile target that runs `python -m milk_component_calculations.pipeline`. The other targets are `make init`, `make check`, `make docs`, and `make clean`. The recipes use Python instead of `rm`, so they work on Windows, macOS, and Linux.

**How a reviewer should set up and execute the project**

The six commands listed under Milestone 4 are the complete setup. There are no other steps. GitHub Actions repeats the lint, the tests, and the example workflow on a clean machine for Python 3.11 and 3.12.

**What remains before the release-candidate stage**

- Compare the results with the original analysis of the trial data.
- Finish the paper and the reflections in `paper/`.
- Remove the template files that the project does not use.
