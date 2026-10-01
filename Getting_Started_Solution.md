
---

# EHR AI Architecture: Hybrid Search, Security & Guardrails

## 1. System Setup & Data Ingestion

* **Database Infrastructure:** Patient data is ingested into a **PostgreSQL** database hosted on an AWS **EC2 Instance**.

* **Database Name:** `hospital_db`.

* **Vector Extension `pgvector`):**

* Instead of building a separate, complex RAG pipeline with a external vector database, we use PostgreSQL's native extension: `pgvector`.

 **`pgvector` *allows storing vector embeddings directly alongside structured relational data and performs* *Cosine Similarity** searches within PostgreSQL.

* **Forward-Deployed Engineering Mindset:** Beginners unnecessarily split systems into separate relational and vector databases. A senior engineer simplifies architecture by keeping structured EHR data and unstructured embedding notes together in PostgreSQL via `pgvector`.

---

## 2. Query & Search Flow (Hybrid Search Approach)

To optimize query performance across huge datasets (e.g., 25+ million rows), the system uses a **Hybrid Search Approach**:

```

 ┌──────────────────────────────────────┐

 │  Doctor Selects Patient (e.g., ID)   │  ──▶  Filters 25M rows down

 └──────────────────┬───────────────────┘       to ~100 patient rows

                    │

                    ▼

 ┌──────────────────────────────────────┐

 │   pgvector Cosine Similarity Search   │  ──▶  Extracts relevant notes

 └──────────────────┬───────────────────┘       for THAT patient only

                    │

                    ▼

 ┌──────────────────────────────────────┐

 │     Redaction Layer (Presidio)       │  ──▶  Masks/removes PHI

 └──────────────────┬───────────────────┘       from the 100 rows

                    │

                    ▼

 ┌──────────────────────────────────────┐

 │   Input Guardrails (NeMo Guardrails) │  ──▶  Validates prompt safety

 └──────────────────┬───────────────────┘       (Blocks illegal queries)

                    │

                    ▼

 ┌──────────────────────────────────────┐

 │  LLM Processing & Clinical Response  │  ──▶  Returns safe answer

 └──────────────────────────────────────┘       to the doctor

```

### Why Pure Vector Search Fails at Scale

* Running a global similarity search against 25 million clinical rows for every query is extremely slow and compute-expensive.

### The Hybrid Solution

1. **Relational Pre-Filtering:** The doctor selects a specific patient (e.g., via a patient ID drop-down).

2. **Targeted Vector Search:** The similarity search runs **only** against that specific patient's historical records (narrowing 25 million rows down to ~100 relevant clinical rows).

3. **Outcome:** Dramatically reduces latency, database load, and compute costs.

---

## 3. Data Privacy & Security (Redaction)

Before sending the retrieved search results (the ~100 context rows) to an LLM, the system enforces **Data Redaction** (Masking):

* **Redaction Process:** Removing or masking all **Protected Health Information (PHI)** and **Personally Identifiable Information (PII)**—such as patient names, phone numbers, addresses, and ID numbers—from the retrieved text.

* **Technology Used:** **Microsoft Presidio** (an open-source data protection and anonymization engine).

* **Goal:** Ensures raw demographic or identifiable patient data is never exposed to external LLM endpoints.

---

## 4. Input Guardrails & Clinical Safety

### The Problem Scenario

A doctor submits a high-risk query: *"What medicine should I prescribe to this patient?"*

### Why We Need Guardrails

* **Medical Risk & Liability:** LLMs must **not** make direct diagnostic or prescription decisions. Would you want a doctor prescribing your medication solely based on an AI prompt?

* **NVIDIA NeMo Guardrails Integration:**

* Acts as a programmable security checkpoint sitting between the doctor's question and the LLM.

* **Unsafe / High-Risk Query:** If a query violates clinical rules (e.g., asking the LLM to directly dictate a prescription), NeMo Guardrails **rejects the query immediately** and stops execution.

* **Safe Query:** If the question passes safety checks (e.g., *"Summarize this patient's past allergies"*), NeMo combines the question with the redacted patient context and routes it to the LLM.

---

## Technical Terminology Fixes & Corrections Summary

| Original Note Term | Corrected Technical Term | Explanation |

| --- | --- | --- |

| `Reduction` | **Redaction** | The process of removing or obscuring sensitive text (PHI/PII) for security. |

| `Microsoft precides` | **Microsoft Presidio** | Microsoft's open-source library for PII/PHI detection and anonymization. |

| `nemo guardrails` | **NVIDIA NeMo Guardrails** | An open-source toolkit for adding safety and security rails to LLM applications. |

| `PostgresSql` | **PostgreSQL** | Standardized casing for the relational database. |

| `pg_vector` | *`pgvector`** | The official name of the vector similarity search extension for PostgreSQL. |