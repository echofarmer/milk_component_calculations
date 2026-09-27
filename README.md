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

