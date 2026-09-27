# Project Proposal

Jessica Duran

## Summary

This project will develop a Python package that combines milk-component records (fat, protein, and lactose percentages per cow per milking, from Excel exports) with milk-yield records (milk per cow per
milking, from CSV exports). The software will check both sources for missing, duplicated, and implausible values, match them by cow, date, and milking, and calculate fat, protein, and lactose yield for each
milking. It will also produce summary tables and basic graphs and export a clean, merged dataset. The purpose is to replace a manual spreadsheet and notebook process with a workflow that is accurate, transparent, and reproducible.

## Overview

Dairy farms and researchers collect milk-production data from more than one system. Milking-parlor software records how much milk each cow gives at each milking, while a laboratory reports the fat, protein, and lactose percentages of milk samples taken at selected milkings. Before these records can be used for research or herd management, the two sources must be combined and checked for missing values, duplicated observations, inconsistent units, and biologically implausible measurements. For example, calculating kilograms of fat produced at a milking requires both the milk weight from the parlor
system and the fat percentage from the laboratory for that same cow and milking. Performing these steps by hand in spreadsheets is slow, inconsistent, and difficult to reproduce. A documented software workflow will make the analysis faster, more accurate, and repeatable.


## Software or Project Description

The software will import milk-component Excel exports and milk-yield CSV exports, standardize their column names and data types, combine repeated milk-yield records within a milking, and match the two sources by cow, date, and milking before calculating component yields.

The intended users are dairy researchers, students, veterinarians, Extension professionals, and farm advisers who need a consistent way to prepare and summarize milk-production records. The expected impact is a faster, more transparent, and reproducible workflow that reduces calculation errors and makes dairy data easier to analyze than repeated manual spreadsheet procedures.


## Project Goals and Timeline

The project is organized around the course milestones.

Milestone 1: Project Setup (completed). The repository contains a clear project structure, a proposal, and a README.

Milestone 2: Initial Prototype (completed). By the second milestone, the software will load both data sources, check data quality, and clean the data.

Milestone 3: Testing and Validation Baseline. The software will merge the two sources by cow, date, and milking and calculate fat, protein, and lactose yield per milking. Automated tests will confirm
that calculated yields match hand-calculated values and that each data-quality check catches the problem it targets. The project will document its assumptions, limitations, and known edge cases, such as partially sampled days and records that appear in only one source.

Milestone 4: Documentation and Reproducibility Pass. The README will explain installation, setup, and the full workflow, with example inputs and outputs. All core functions will have docstrings. Example data files that follow the real export formats will let a reviewer reproduce the results.

Milestone 5: Project Systems and Automation (November 8, 2026). The full workflow will run from the repository root through Makefile commands for environment setup, checks, and execution, starting from a clean copy of the repository without undocumented steps.


## Methods and Workflow

Milk yield is recorded per milking, and component samples are taken for only some milkings. Component yield is therefore calculated per milking (yield = milk kg × component % / 100). Daily totals are reported only for cow-days on which every milking was sampled, so that partially sampled days are not underestimated. Milk recorded in pounds is converted to kilograms before calculation.


## Anticipated Challenges

Dairy datasets may use different column names, formats, and measurement units. Milk may be recorded in pounds instead of kilograms, and component values may be stored as percentages or decimals. The software will require users to state the units and will map input columns to a documented standard format before calculations are performed.

Component values of zero represent failed or missing samples rather than true zeros and will be  converted to missing values. Records present in only one source cannot be merged; the software will report how many records each source loses so that excluded data are visible rather than silently dropped.

## Expected Outcomes

By the end of the semester, the project will provide a tested and documented Python package that converts milk-component and milk-yield exports into a clean, merged dataset with fat, protein, and lactose yields per milking, summary tables, basic graphs, and a data-quality report.

Success will be measured by:

1. automated tests showing that calculated yields match hand-calculated values for known inputs
2. reproducing the merged dataset produced by the original analysis notebook
3. a data-quality report that lists every flagged or excluded record