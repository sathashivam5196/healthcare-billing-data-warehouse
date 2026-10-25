\# Healthcare Billing Data Model



\## Overview



This entity relationship diagram (ERD) illustrates the nine synthetic healthcare billing entities used in the project.



The diagram represents the logical relationships between patients, providers, encounters, claims, claim lines, payers, payments, denials, and adjustments.



\## Entity Relationship Diagram



```mermaid

erDiagram

&#x20;   PATIENT ||--o{ ENCOUNTER : has

&#x20;   PROVIDER ||--o{ ENCOUNTER : serves

&#x20;   ENCOUNTER ||--o{ CLAIM : generates

&#x20;   PAYER ||--o{ CLAIM : processes

&#x20;   CLAIM ||--o{ CLAIM\_LINE : contains

&#x20;   CLAIM ||--o{ PAYMENT : receives

&#x20;   PAYER ||--o{ PAYMENT : provides

&#x20;   CLAIM ||--o{ DENIAL : may\_have

&#x20;   CLAIM ||--o{ ADJUSTMENT : may\_have



&#x20;   PATIENT {

&#x20;       int patient\_id PK

&#x20;   }



&#x20;   PROVIDER {

&#x20;       int provider\_id PK

&#x20;   }



&#x20;   PAYER {

&#x20;       int payer\_id PK

&#x20;       string payer\_code

&#x20;       string payer\_name

&#x20;       string payer\_type

&#x20;   }



&#x20;   ENCOUNTER {

&#x20;       int encounter\_id PK

&#x20;       int patient\_id FK

&#x20;       int provider\_id FK

&#x20;       date service\_date

&#x20;       string encounter\_type

&#x20;       int place\_of\_service

&#x20;       string encounter\_status

&#x20;   }



&#x20;   CLAIM {

&#x20;       int claim\_id PK

&#x20;       int encounter\_id FK

&#x20;       int payer\_id FK

&#x20;       string claim\_number

&#x20;       date submitted\_date

&#x20;       string claim\_status

&#x20;       double billed\_amount

&#x20;       double allowed\_amount

&#x20;       double patient\_responsibility

&#x20;   }



&#x20;   CLAIM\_LINE {

&#x20;       int claim\_line\_id PK

&#x20;       int claim\_id FK

&#x20;   }



&#x20;   PAYMENT {

&#x20;       int payment\_id PK

&#x20;       int claim\_id FK

&#x20;       int payer\_id FK

&#x20;       date payment\_date

&#x20;       double payment\_amount

&#x20;       string posting\_status

&#x20;   }



&#x20;   DENIAL {

&#x20;       int denial\_id PK

&#x20;       int claim\_id FK

&#x20;       date denial\_date

&#x20;       string denial\_code

&#x20;       string denial\_category

&#x20;       string denial\_status

&#x20;   }



&#x20;   ADJUSTMENT {

&#x20;       int adjustment\_id PK

&#x20;       int claim\_id FK

&#x20;   }

```



\## Entity Descriptions



| Entity | Purpose |

|---|---|

| Patient | Stores synthetic patient identifiers. |

| Provider | Identifies healthcare service providers. |

| Payer | Represents insurance payers and self-pay. |

| Encounter | Represents a patient service event. |

| Claim | Records billing claims associated with encounters and payers. |

| Claim line | Represents individual lines within a claim. |

| Payment | Records claim payments and posting status. |

| Denial | Records claim denial details, codes, and status. |

| Adjustment | Represents claim-related billing adjustments. |



\## Key Relationships



\- A patient can have multiple encounters.

\- A provider can serve multiple encounters.

\- An encounter can be associated with multiple claims.

\- A payer can be associated with multiple claims and payments.

\- A claim can contain multiple claim lines.

\- A claim can have multiple payments, denials, and adjustments.



\## Data Model Notes



\- All project data is synthetic.

\- `PK` indicates a primary key; `FK` indicates a foreign key.

\- The diagram describes the logical relationships used for portfolio documentation. Verify the exact database constraints and optional relationships against the implemented schema before treating the diagram as a formal database constraint specification.

