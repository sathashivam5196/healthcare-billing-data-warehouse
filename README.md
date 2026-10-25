# Healthcare Billing Data Warehouse & Analytics Pipeline

## Overview

An end-to-end data engineering and analytics portfolio project built using synthetic healthcare billing data. This project demonstrates relational data modeling, Python-based data generation, PostgreSQL warehousing, data quality validation, CSV-based data ingestion, Databricks SQL analytics, and dashboard development.

**All data is synthetic. No real patient information is used.**

## Technology Stack

- Python
- PostgreSQL 18
- SQL
- PowerShell
- Databricks SQL
- Unity Catalog
- Git and GitHub

## Architecture

1. Generate synthetic healthcare billing data using Python.
2. Load and organize data in PostgreSQL.
3. Structure data into raw, staging, warehouse, and reporting schemas.
4. Validate relationships, billing amounts, and data consistency.
5. Export nine warehouse tables to CSV.
6. Upload CSV files to a Databricks Unity Catalog volume.
7. Create Databricks tables and reconcile source and destination row counts.
8. Develop reporting views for collections, denials, payer performance, and claim-level financial analysis.
9. Build and publish a Healthcare Billing Analytics Dashboard.

## Data Model

The project contains nine warehouse entities:

- Patient
- Provider
- Payer
- Encounter
- Claim
- Claim line
- Payment
- Denial
- Adjustment

## Data Volume

| Entity | Records |
|---|---:|
| Patient | 10,000 |
| Provider | 5 |
| Payer | 5 |
| Encounter | 18,107 |
| Claim | 17,250 |
| Claim line | 34,438 |
| Payment | 8,575 |
| Denial | 2,046 |
| Adjustment | 3,460 |

**Total records across the nine entities:** 93,886.

## PostgreSQL Reporting Views

The PostgreSQL reporting layer contains:

- `reporting.claim_ar`
- `reporting.denial_summary`
- `reporting.monthly_collections`
- `reporting.payer_performance`

## Databricks Implementation

**Catalog:** `workspace`  
**Schema:** `workspace.healthcare_billing`  
**CSV volume:** `billing_csv_files`

All nine CSV files were uploaded to the Databricks Unity Catalog volume and imported into Databricks tables.

### Imported Tables

The following source and destination row counts were reconciled successfully:

| Table | Validated row count |
|---|---:|
| `patient` | 10,000 |
| `provider` | 5 |
| `payer` | 5 |
| `encounter` | 18,107 |
| `claim` | 17,250 |
| `claim_line` | 34,438 |
| `payment` | 8,575 |
| `denial` | 2,046 |
| `adjustment` | 3,460 |

### Databricks Reporting Views

Four reporting views were created and queried successfully:

- `workspace.healthcare_billing.monthly_collections` — monthly payment counts, collections, and average payment amounts.
- `workspace.healthcare_billing.denial_summary` — denial counts by month, category, denial code, and status.
- `workspace.healthcare_billing.payer_performance` — claim volumes, billed amounts, allowed amounts, patient responsibility, and allowed-to-billed percentages by payer.
- `workspace.healthcare_billing.claim_ar` — claim-level financial details enriched with encounter and payer information.

### Dashboard

The **Healthcare Billing Analytics Dashboard** was published in Databricks.

The dashboard includes visualizations for:

- Monthly collections trends
- Claim counts by status
- Billed amounts by payer
- Denials by category

The dashboard is published in Databricks. Viewer access remains subject to the configured sharing permissions.

## Data Quality and Validation

The PostgreSQL workflow includes checks for:

- Claims referencing missing encounters
- Claim lines and transactions referencing missing claims
- Claim billed-amount consistency
- Future-dated payments
- Table row counts
- Backup and restore consistency

The Databricks workflow includes:

- Reconciliation of all nine imported table counts against PostgreSQL.
- Denial summary reconciliation against all 2,046 source denial records.
- Claim-level validation confirming 17,250 distinct claims in `claim_ar`.
- Billed amount reconciliation between the source claim table and `claim_ar`, with both totals equal to 16,390,165.10.

## Repository Contents

- `scripts/` — Python data generation, connection, and validation scripts.
- `README.md` — Project documentation.
- `.gitignore` — Excludes local data, backups, virtual environments, and generated files.

## Future Enhancements

- Add reproducible PostgreSQL and Databricks setup instructions.
- Add dashboard screenshots and architecture documentation.
- Develop automated incremental ingestion.
- Expand data quality monitoring and reporting.
- Document the SQL definitions for all reporting views in the repository.

## Data Privacy

This project is intended for learning and portfolio demonstration. Only synthetic data should be committed to the repository. Database credentials, local backups, and other sensitive configuration files must remain outside version control.
