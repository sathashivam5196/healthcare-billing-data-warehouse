--
-- PostgreSQL database dump
--

\restrict EE5yLjhVgZXBnwOWoCuAZNLxnnypMr9k1VIJdHlqjVcqAlbQ5UAh07hL2fbFRG3

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: warehouse; Type: SCHEMA; Schema: -; Owner: -
--



SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: adjustment; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.adjustment (
    adjustment_id bigint NOT NULL,
    claim_id bigint NOT NULL,
    adjustment_date date NOT NULL,
    adjustment_code character varying(30) NOT NULL,
    adjustment_type character varying(20) NOT NULL,
    adjustment_amount numeric(12,2) NOT NULL,
    CONSTRAINT adjustment_adjustment_amount_check CHECK ((adjustment_amount >= (0)::numeric)),
    CONSTRAINT adjustment_adjustment_type_check CHECK (((adjustment_type)::text = ANY ((ARRAY['Contractual'::character varying, 'WriteOff'::character varying, 'Correction'::character varying, 'Other'::character varying])::text[])))
);


--
-- Name: claim; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.claim (
    claim_id bigint NOT NULL,
    encounter_id bigint NOT NULL,
    payer_id integer NOT NULL,
    claim_number character varying(40) NOT NULL,
    submitted_date date NOT NULL,
    claim_status character varying(20) NOT NULL,
    billed_amount numeric(12,2) NOT NULL,
    allowed_amount numeric(12,2) NOT NULL,
    patient_responsibility numeric(12,2) NOT NULL,
    CONSTRAINT claim_allowed_amount_check CHECK ((allowed_amount >= (0)::numeric)),
    CONSTRAINT claim_billed_amount_check CHECK ((billed_amount >= (0)::numeric)),
    CONSTRAINT claim_claim_status_check CHECK (((claim_status)::text = ANY ((ARRAY['Submitted'::character varying, 'Accepted'::character varying, 'Denied'::character varying, 'Paid'::character varying, 'PartiallyPaid'::character varying, 'Rejected'::character varying, 'Pending'::character varying])::text[]))),
    CONSTRAINT claim_patient_responsibility_check CHECK ((patient_responsibility >= (0)::numeric))
);


--
-- Name: encounter; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.encounter (
    encounter_id bigint NOT NULL,
    patient_id bigint NOT NULL,
    provider_id integer NOT NULL,
    service_date date NOT NULL,
    encounter_type character varying(50) NOT NULL,
    place_of_service character varying(10) NOT NULL,
    encounter_status character varying(20) NOT NULL,
    CONSTRAINT encounter_encounter_status_check CHECK (((encounter_status)::text = ANY ((ARRAY['Completed'::character varying, 'Cancelled'::character varying, 'InProgress'::character varying])::text[])))
);


--
-- Name: payer; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.payer (
    payer_id integer NOT NULL,
    payer_code character varying(30) NOT NULL,
    payer_name character varying(100) NOT NULL,
    payer_type character varying(20) NOT NULL,
    CONSTRAINT payer_payer_type_check CHECK (((payer_type)::text = ANY ((ARRAY['Commercial'::character varying, 'Medicare'::character varying, 'Medicaid'::character varying, 'SelfPay'::character varying])::text[])))
);


--
-- Name: payment; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.payment (
    payment_id bigint NOT NULL,
    claim_id bigint NOT NULL,
    payer_id integer NOT NULL,
    payment_date date NOT NULL,
    payment_method character varying(30) NOT NULL,
    payment_amount numeric(12,2) NOT NULL,
    posting_status character varying(15) NOT NULL,
    CONSTRAINT payment_payment_amount_check CHECK ((payment_amount > (0)::numeric)),
    CONSTRAINT payment_posting_status_check CHECK (((posting_status)::text = ANY ((ARRAY['Posted'::character varying, 'Pending'::character varying, 'Reversed'::character varying])::text[])))
);


--
-- Name: denial; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.denial (
    denial_id bigint NOT NULL,
    claim_id bigint NOT NULL,
    denial_date date NOT NULL,
    denial_code character varying(20) NOT NULL,
    denial_category character varying(50) NOT NULL,
    denial_status character varying(20) NOT NULL,
    CONSTRAINT denial_denial_status_check CHECK (((denial_status)::text = ANY ((ARRAY['Open'::character varying, 'Appealed'::character varying, 'Resolved'::character varying, 'WrittenOff'::character varying])::text[])))
);


--
-- Name: claim_line; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.claim_line (
    claim_line_id bigint NOT NULL,
    claim_id bigint NOT NULL,
    line_number smallint NOT NULL,
    procedure_code character varying(20) NOT NULL,
    diagnosis_code character varying(20) NOT NULL,
    units numeric(8,2) NOT NULL,
    charge_amount numeric(12,2) NOT NULL,
    allowed_amount numeric(12,2) NOT NULL,
    CONSTRAINT claim_line_allowed_amount_check CHECK ((allowed_amount >= (0)::numeric)),
    CONSTRAINT claim_line_charge_amount_check CHECK ((charge_amount >= (0)::numeric)),
    CONSTRAINT claim_line_units_check CHECK ((units > (0)::numeric))
);


--
-- Name: patient; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.patient (
    patient_id bigint NOT NULL,
    synthetic_patient_key character varying(30) NOT NULL,
    birth_date date NOT NULL,
    sex_at_birth character(1) NOT NULL,
    postal_code character varying(10) NOT NULL,
    CONSTRAINT patient_sex_at_birth_check CHECK ((sex_at_birth = ANY (ARRAY['F'::bpchar, 'M'::bpchar, 'X'::bpchar, 'U'::bpchar])))
);


--
-- Name: provider; Type: TABLE; Schema: warehouse; Owner: -
--

CREATE TABLE warehouse.provider (
    provider_id integer NOT NULL,
    provider_npi character varying(10) NOT NULL,
    provider_name character varying(150) NOT NULL,
    provider_type character varying(50) NOT NULL,
    state_code character(2) NOT NULL
);


--
-- Name: adjustment adjustment_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.adjustment
    ADD CONSTRAINT adjustment_pkey PRIMARY KEY (adjustment_id);


--
-- Name: claim claim_claim_number_key; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim
    ADD CONSTRAINT claim_claim_number_key UNIQUE (claim_number);


--
-- Name: claim claim_encounter_id_key; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim
    ADD CONSTRAINT claim_encounter_id_key UNIQUE (encounter_id);


--
-- Name: claim_line claim_line_claim_id_line_number_key; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim_line
    ADD CONSTRAINT claim_line_claim_id_line_number_key UNIQUE (claim_id, line_number);


--
-- Name: claim_line claim_line_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim_line
    ADD CONSTRAINT claim_line_pkey PRIMARY KEY (claim_line_id);


--
-- Name: claim claim_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim
    ADD CONSTRAINT claim_pkey PRIMARY KEY (claim_id);


--
-- Name: denial denial_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.denial
    ADD CONSTRAINT denial_pkey PRIMARY KEY (denial_id);


--
-- Name: encounter encounter_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.encounter
    ADD CONSTRAINT encounter_pkey PRIMARY KEY (encounter_id);


--
-- Name: patient patient_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);


--
-- Name: patient patient_synthetic_patient_key_key; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.patient
    ADD CONSTRAINT patient_synthetic_patient_key_key UNIQUE (synthetic_patient_key);


--
-- Name: payer payer_payer_code_key; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.payer
    ADD CONSTRAINT payer_payer_code_key UNIQUE (payer_code);


--
-- Name: payer payer_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.payer
    ADD CONSTRAINT payer_pkey PRIMARY KEY (payer_id);


--
-- Name: payment payment_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);


--
-- Name: provider provider_pkey; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.provider
    ADD CONSTRAINT provider_pkey PRIMARY KEY (provider_id);


--
-- Name: provider provider_provider_npi_key; Type: CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.provider
    ADD CONSTRAINT provider_provider_npi_key UNIQUE (provider_npi);


--
-- Name: idx_adjustment_claim; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_adjustment_claim ON warehouse.adjustment USING btree (claim_id);


--
-- Name: idx_claim_line_claim; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_claim_line_claim ON warehouse.claim_line USING btree (claim_id);


--
-- Name: idx_claim_payer_status; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_claim_payer_status ON warehouse.claim USING btree (payer_id, claim_status);


--
-- Name: idx_claim_submitted_date; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_claim_submitted_date ON warehouse.claim USING btree (submitted_date);


--
-- Name: idx_denial_status_date; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_denial_status_date ON warehouse.denial USING btree (denial_status, denial_date);


--
-- Name: idx_encounter_patient_date; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_encounter_patient_date ON warehouse.encounter USING btree (patient_id, service_date);


--
-- Name: idx_encounter_service_date; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_encounter_service_date ON warehouse.encounter USING btree (service_date);


--
-- Name: idx_payment_claim_date; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_payment_claim_date ON warehouse.payment USING btree (claim_id, payment_date);


--
-- Name: idx_payment_posting_date; Type: INDEX; Schema: warehouse; Owner: -
--

CREATE INDEX idx_payment_posting_date ON warehouse.payment USING btree (posting_status, payment_date);


--
-- Name: adjustment adjustment_claim_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.adjustment
    ADD CONSTRAINT adjustment_claim_id_fkey FOREIGN KEY (claim_id) REFERENCES warehouse.claim(claim_id);


--
-- Name: claim claim_encounter_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim
    ADD CONSTRAINT claim_encounter_id_fkey FOREIGN KEY (encounter_id) REFERENCES warehouse.encounter(encounter_id);


--
-- Name: claim_line claim_line_claim_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim_line
    ADD CONSTRAINT claim_line_claim_id_fkey FOREIGN KEY (claim_id) REFERENCES warehouse.claim(claim_id);


--
-- Name: claim claim_payer_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.claim
    ADD CONSTRAINT claim_payer_id_fkey FOREIGN KEY (payer_id) REFERENCES warehouse.payer(payer_id);


--
-- Name: denial denial_claim_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.denial
    ADD CONSTRAINT denial_claim_id_fkey FOREIGN KEY (claim_id) REFERENCES warehouse.claim(claim_id);


--
-- Name: encounter encounter_patient_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.encounter
    ADD CONSTRAINT encounter_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES warehouse.patient(patient_id);


--
-- Name: encounter encounter_provider_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.encounter
    ADD CONSTRAINT encounter_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES warehouse.provider(provider_id);


--
-- Name: payment payment_claim_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.payment
    ADD CONSTRAINT payment_claim_id_fkey FOREIGN KEY (claim_id) REFERENCES warehouse.claim(claim_id);


--
-- Name: payment payment_payer_id_fkey; Type: FK CONSTRAINT; Schema: warehouse; Owner: -
--

ALTER TABLE ONLY warehouse.payment
    ADD CONSTRAINT payment_payer_id_fkey FOREIGN KEY (payer_id) REFERENCES warehouse.payer(payer_id);


--
-- PostgreSQL database dump complete
--

\unrestrict EE5yLjhVgZXBnwOWoCuAZNLxnnypMr9k1VIJdHlqjVcqAlbQ5UAh07hL2fbFRG3

