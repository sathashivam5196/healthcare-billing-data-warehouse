# Healthcare Billing Data Warehouse & Analytics Pipeline

## Overview

An end-to-end data engineering portfolio project using synthetic healthcare billing data. The project demonstrates relational data modeling, ETL development, SQL reporting, data quality validation, and cloud analytics preparation.

**All data is synthetic. No real patient information is used.**

## Technology Stack

- Python
- PostgreSQL 18
- SQL
- PowerShell
- Databricks SQL
- Git and GitHub

## Architecture

1. Generate synthetic healthcare billing data using Python.
2. Load and organize data in PostgreSQL.
3. Structure data into raw, staging, warehouse, and reporting schemas.
4. Validate relationships, billing amounts, and data consistency.
5. Export warehouse tables to CSV.
6. Upload the CSV files to a Databricks Unity Catalog volume.
7. Create Databricks tables and reporting views.
8. Build a healthcare billing analytics dashboard.

## Data Model

The project includes nine warehouse entities:

- Patient
- Provider
- Payer
- Encounter
- Claim
- Claim line
- Payment
- Denial
- Adjustment

## PostgreSQL Reporting Views

- `reporting.claim_ar`
- `reporting.denial_summary`
- `reporting.monthly_collections`
- `reporting.payer_performance`

## Validation

The local PostgreSQL workflow includes checks for:

- Missing encounter references in claims
- Missing claim references in claim lines and transactions
- Claim billed-amount consistency
- Future-dated payments
- Table row counts
- Backup and restore consistency

## Project Status

**PostgreSQL:** Synthetic data loading, reporting views, data-quality checks, and backup/restore validation completed.

**Databricks:** Created the `workspace.healthcare_billing` schema and `billing_csv_files` volume. All nine CSV files have been uploaded. Table creation, row-count reconciliation, reporting views, and dashboard development are pending.

## Repository Contents

- `scripts/` — Python data generation, connection, and validation scripts
- `README.md` — Project documentation
- `.gitignore` — Excludes local data, backups, environments, and generated files

## Planned Enhancements

- Create Databricks tables from the uploaded CSV files.
- Reconcile source and destination row counts.
- Implement reporting views in Databricks SQL.
- Build a dashboard for accounts receivable, collections, denials, and payer performance.
- Add reproducible setup instructions and architecture documentation.
- Explore automated incremental ingestion.

## Data Privacy

This project is intended for learning and portfolio demonstration. Only synthetic data should be committed to the repository.
