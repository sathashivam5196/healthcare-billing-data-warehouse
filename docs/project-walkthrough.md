\# Healthcare Billing Data Warehouse — Project Walkthrough



\## 1. Project Overview



This project demonstrates an end-to-end healthcare billing analytics pipeline built with synthetic data. It combines Python, PostgreSQL, SQL, CSV-based data transfer, Databricks SQL, and a published analytics dashboard.



\*\*Objective:\*\* Build a reproducible data workflow that organizes healthcare billing records, validates data quality, and produces reporting outputs for billing analysis.



All data used in this project is synthetic. No real patient information is included.



\## 2. Technology Stack



\- \*\*Python:\*\* Synthetic data generation and supporting scripts.

\- \*\*PostgreSQL 18:\*\* Relational storage, warehouse modeling, and SQL reporting.

\- \*\*SQL:\*\* Data validation, aggregations, joins, and reporting views.

\- \*\*CSV:\*\* Data transfer from PostgreSQL exports to Databricks.

\- \*\*Databricks SQL:\*\* Cloud-based tables, reporting views, and analytics.

\- \*\*Unity Catalog:\*\* Organization and storage of the imported CSV files.

\- \*\*Git and GitHub:\*\* Version control and portfolio documentation.



\## 3. Pipeline Walkthrough



\### Step 1 — Generate synthetic data



Python scripts generate sample healthcare billing entities, including patients, providers, payers, encounters, claims, claim lines, payments, denials, and adjustments.



The synthetic data provides a realistic structure for demonstrating billing analytics without using real patient records.



\### Step 2 — Store and organize data in PostgreSQL



The generated records are loaded into the `healthcare\_billing` PostgreSQL database.



The database organizes the data into four schemas:



\- `raw`

\- `staging`

\- `warehouse`

\- `reporting`



This structure separates data organization and warehouse entities from reporting logic.



\### Step 3 — Validate the data



Data quality checks and row-count comparisons help verify that records have loaded as expected.



The project also includes database backup and restore validation.



\### Step 4 — Export data to CSV



Warehouse tables are exported to CSV files for transfer to Databricks.



CSV provides a simple, inspectable transfer format for this portfolio implementation.



\### Step 5 — Ingest data into Databricks



The CSV files are uploaded to a Databricks Unity Catalog volume and imported into Databricks tables.



The imported row counts were reconciled against the PostgreSQL source counts.



\### Step 6 — Create SQL reporting views



Four reporting views support different billing analytics use cases:



| View | Purpose |

|---|---|

| `monthly\_collections` | Summarizes payment counts, collection amounts, and average payment amounts by month. |

| `denial\_summary` | Groups denials by month, category, code, and status. |

| `payer\_performance` | Summarizes claim volume and billed, allowed, and patient-responsibility amounts by payer. |

| `claim\_ar` | Combines claim, encounter, and payer details for claim-level reporting. |



The SQL definitions are maintained in the repository's `sql/` directory.



\*\*Metric note:\*\* The `claim\_ar` view includes billed amount less allowed amount. This is a reporting calculation and should not be interpreted as actual outstanding accounts receivable because payments and adjustments are not deducted in that expression.



\### Step 7 — Build the analytics dashboard



The Healthcare Billing Analytics Dashboard was published in Databricks.



Its visualizations include:



\- Monthly collections trends.

\- Claim counts by status.

\- Billed amount by payer.

\- Denials by category.

\- Payer performance details.



Dashboard access is governed by the configured Databricks sharing permissions.



\## 4. Dataset Scale



The implemented Databricks tables were validated against the following source counts:



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

| \*\*Total\*\* | \*\*93,886\*\* |



These are synthetic records used to demonstrate the pipeline.



\## 5. Validation Results



The project includes the following checks:



\- Reconciliation of PostgreSQL export counts with Databricks table counts.

\- Validation of reporting-view row counts.

\- Reconciliation of denial summary counts against the source denial records.

\- Reconciliation of claim counts and billed totals in the claim-level reporting view.

\- PostgreSQL backup and restore testing.



These checks help demonstrate data integrity across the implemented workflow.



\## 6. Repository Guide



\- `generate\_synthetic\_data.py` — generates synthetic data.

\- `generate\_incremental\_data.py` — supports incremental synthetic data generation.

\- `check\_tables.py` — checks database tables.

\- `check\_row\_counts.py` — checks row counts.

\- `check\_load\_state.py` — checks load state.

\- `test\_connection.py` — tests the database connection.

\- `sql/` — contains the four Databricks SQL reporting view definitions.

\- `docs/architecture.md` — explains the data flow and architecture.

\- `docs/screenshots/` — contains the dashboard screenshot.



\## 7. Skills Demonstrated



\- Relational data modeling.

\- Python-based synthetic data generation.

\- PostgreSQL and SQL reporting.

\- Data quality and reconciliation checks.

\- CSV-based data transfer.

\- Databricks table ingestion and SQL analytics.

\- Dashboard development.

\- Git version control and technical documentation.



\## 8. Potential Future Improvements



\- Automate the PostgreSQL-to-Databricks ingestion process.

\- Add orchestration and scheduled pipeline execution.

\- Add automated data quality tests.

\- Introduce incremental ingestion and change tracking.

\- Add documented deployment and environment setup instructions.



These are future enhancements and are not represented as completed features of the current implementation.

