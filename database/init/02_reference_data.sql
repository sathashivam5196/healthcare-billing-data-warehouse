INSERT INTO warehouse.provider
    (provider_id, provider_npi, provider_name, provider_type, state_code)
VALUES
    (1, '1000000001', 'Northside Medical Group', 'Clinic', 'MN'),
    (2, '1000000002', 'Lakeview Emergency Services', 'Emergency', 'WI'),
    (3, '1000000003', 'Metro Specialty Care', 'Specialty', 'IL'),
    (4, '1000000004', 'Community Health Partners', 'Hospital', 'IA'),
    (5, '1000000005', 'Riverbend Family Practice', 'Clinic', 'MI');

INSERT INTO warehouse.payer
    (payer_id, payer_code, payer_name, payer_type)
VALUES
    (1, 'COMM_A', 'Northstar Commercial', 'Commercial'),
    (2, 'COMM_B', 'Pioneer Health Plan', 'Commercial'),
    (3, 'MEDICARE', 'Synthetic Medicare', 'Medicare'),
    (4, 'MEDICAID', 'Synthetic Medicaid', 'Medicaid'),
    (5, 'SELFPAY', 'Self Pay', 'SelfPay');
