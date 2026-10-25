\# Healthcare Billing Data Warehouse Architecture



\## Overview



This architecture shows how synthetic healthcare billing data moves from Python generation through PostgreSQL warehousing and CSV export into Databricks SQL analytics.



\## Data Flow



```mermaid

flowchart TD

&#x20;   A\["Python Synthetic Data Generator"] --> B\["PostgreSQL Database"]



&#x20;   B --> C\["Raw Schema"]

&#x20;   C --> D\["Staging Schema"]

&#x20;   D --> E\["Warehouse Schema"]

&#x20;   E --> F\["Reporting Schema"]



&#x20;   E --> G\["CSV Export"]

&#x20;   G --> H\["Databricks Unity Catalog Volume"]

&#x20;   H --> I\["Databricks Tables"]



&#x20;   I --> J\["SQL Reporting Views"]



&#x20;   J --> K\["Healthcare Billing Analytics Dashboard"]



&#x20;   L\["Data Quality Validation"] -.-> B

&#x20;   L -.-> I

&#x20;   L -.-> J



&#x20;   style A fill:#DCEAFE,stroke:#2563EB,color:#111827

&#x20;   style B fill:#DCEAFE,stroke:#2563EB,color:#111827

&#x20;   style G fill:#FEF3C7,stroke:#D97706,color:#111827

&#x20;   style I fill:#DCFCE7,stroke:#16A34A,color:#111827

&#x20;   style J fill:#DCFCE7,stroke:#16A34A,color:#111827

&#x20;   style K fill:#EDE9FE,stroke:#7C3AED,color:#111827

```



\## Architecture Components



| Component | Responsibility |

|---|---|

| Python | Generates synthetic healthcare billing data. |

| PostgreSQL | Stores and organizes the source and warehouse data. |

| Raw and staging schemas | Organize data through the database pipeline. |

| Warehouse schema | Stores structured billing entities for analysis. |

| Reporting schema | Provides PostgreSQL reporting views. |

| CSV export | Transfers the warehouse data to Databricks. |

| Unity Catalog volume | Stores the CSV files used for Databricks ingestion. |

| Databricks tables | Provide the imported data for cloud analytics. |

| SQL reporting views | Calculate collections, denial summaries, payer performance, and claim-level reporting. |

| Analytics dashboard | Presents billing metrics through visualizations. |

| Data quality validation | Checks row counts, relationships, and consistency between stages. |



\## Reporting Outputs



The Databricks reporting layer includes:



\- `monthly\_collections` — monthly payment counts and collection amounts.

\- `denial\_summary` — denial counts by period, category, code, and status.

\- `payer\_performance` — payer-level claim and billing metrics.

\- `claim\_ar` — claim-level reporting combining claim, encounter, and payer details.



\## Data Integrity



All project data is synthetic. The pipeline includes row-count reconciliation between PostgreSQL exports and Databricks tables, along with data quality and reporting-view validation.



\*\*Note:\*\* CSV export and Databricks ingestion are the implemented transfer mechanism; this diagram does not imply a live streaming or automatically scheduled integration.

