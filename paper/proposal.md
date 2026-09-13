# Project Proposal

Jessica Duran

## Summary

Provide a short summary of the project and its purpose.This project will develop a Python software package for analyzing raw dairy production data. The software will check the data for missing, duplicated, or invalid values and calculate daily milk-component yields, including fat, protein, and lactose. It will also create summary tables and basic graphs and export a clean dataset for further analysis. The purpose is to make dairy-data analysis more accurate, efficient, transparent, and reproducible than performing the calculations manually in spreadsheets.

## Overview

Dairy farms and researchers collect raw milk-production data containing measurements such as milk yield and the percentages of fat, protein, and lactose. Before these records can be used for research or management, they must be checked for missing values, duplicated observations, incorrect units, and biologically unrealistic measurements. This project will develop a Python software package that imports raw dairy data, performs basic quality checks, and calculates milk-component yields. For example, the software will calculate kilograms of fat and protein produced per cow per day from milk yield and component percentages. It will also generate summary tables and simple visualizations showing how milk production and composition change across cows, herds, or dates. This work matters because manual spreadsheet calculations can be slow, inconsistent, and difficult to reproduce. A documented software workflow will make the analysis faster, more accurate, transparent, and repeatable.

## Software or Project Description

The software will import CSV files, verify that required columns are present, identify missing or duplicated records, and calculate daily milk-component yields.
The intended users are dairy researchers, students, veterinarians, Extension professionals, and farm advisers who need a consistent way to prepare and summarize milk-production records. The expected impact is a faster, more transparent, and reproducible workflow that reduces calculation errors and makes dairy data easier to analyze than relying on repeated manual spreadsheet procedures.


## Project Goals and Timeline

The short-term goal is to establish a functional software foundation. By the first milestone, the repository will contain a clear project structure, a proposal, and a README.
The medium-term goal is to create the main analysis workflow. The software will clean the imported data and calculate fat, protein, and lactose yields from milk yield and component percentages.
The long-term goal is to produce a tested, documented, and reusable Python package. By the end of the semester, a user should be able to import a raw dairy CSV file, calculate milk-component yields, create summaries and graphs, and export the results.


## Methods and Workflow

The project will use a step-by-step Python workflow to transform raw dairy-production records into a clean, analysis-ready dataset. The software will first import a CSV or Excel file and verify that it contains the required columns, such as date, cow ID, milk yield, fat percentage, protein percentage, and lactose percentage. It will then identify missing values, duplicated records, and incorrect data types.
After validation, the software will calculate daily milk-component yields. The processed data will then be summarized by cow, herd, or date. The software will generate descriptive statistics, tables, and basic graphs showing milk yield and milk-component results. Finally, it will export a clean CSV file with the results.


## Anticipated Challenges

One challenge is that dairy datasets may use different column names, formats, and measurement units. For example, milk may be recorded in pounds instead of kilograms, and component values may be stored as percentages or decimals. To address this problem, the software will require users to identify the units and map their columns to a documented standard format before calculations are performed.

## Expected Outcomes

By the end of the semester, the project will provide a tested and documented Python software package that converts raw dairy production data into a clean dataset. A user will be able to import a CSV file, check it for missing values, duplicates, invalid data types and calculate daily fat, protein, and lactose yields. The software will also create summary tables and basic graphs by cow, herd, or date and export the processed results.
Success will mean that the milk-component calculations produce the correct results.
