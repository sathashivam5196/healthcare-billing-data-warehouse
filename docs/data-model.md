# Healthcare Billing Data Model

## Entity Relationship Diagram

This diagram shows the logical relationships between the nine synthetic healthcare billing entities.

```mermaid
erDiagram
    PATIENT ||--o{ ENCOUNTER : has
    PROVIDER ||--o{ ENCOUNTER : serves
    ENCOUNTER ||--o{ CLAIM : generates
    PAYER ||--o{ CLAIM : processes
    CLAIM ||--o{ CLAIM_LINE : contains
    CLAIM ||--o{ PAYMENT : receives
    PAYER ||--o{ PAYMENT : provides
    CLAIM ||--o{ DENIAL : may_have
    CLAIM ||--o{ ADJUSTMENT : may_have

    PATIENT {
        int patient_id PK
    }

    PROVIDER {
        int provider_id PK
    }

    PAYER {
        int payer_id PK
        string payer_code
        string payer_name
        string payer_type
    }

    ENCOUNTER {
        int encounter_id PK
        int patient_id FK
        int provider_id FK
        date service_date
        string encounter_type
        string encounter_status
    }

    CLAIM {
        int claim_id PK
        int encounter_id FK
        int payer_id FK
        string claim_number
        date submitted_date
        string claim_status
        double billed_amount
        double allowed_amount
        double patient_responsibility
    }
    CLAIM_LINE {
        int claim_line_id PK
        int claim_id FK
    }

    PAYMENT {
        int payment_id PK
        int claim_id FK
        int payer_id FK
        date payment_date
        double payment_amount
        string posting_status
    }

    DENIAL {
        int denial_id PK
        int claim_id FK
        date denial_date
        string denial_code
        string denial_category
        string denial_status
    }

    ADJUSTMENT {
        int adjustment_id PK
        int claim_id FK
    }
```

## Entity Descriptions

| Entity | Purpose |
|---|---|
| Patient | Synthetic patient identifiers. |
| Provider | Healthcare service providers. |
| Payer | Insurance payers and self-pay. |
| Encounter | Patient service events. |
| Claim | Billing claims associated with encounters and payers. |
| Claim line | Individual lines within a claim. |
| Payment | Claim payment records and posting status. |
| Denial | Denial codes, categories, and statuses. |
| Adjustment | Claim-related billing adjustments. |

## Notes

- All data is synthetic.
- `PK` means primary key; `FK` means foreign key.
- This is a logical diagram. Verify actual database constraints before treating every relationship as a formal constraint.
