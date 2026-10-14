# Phase 3 — Generate Thousands of Embeddings (Bulk Run)

Goal: fill enough `clinical_embedding` values so hybrid / semantic search can work in later phases.

Phase 2 was about choosing the model and understanding the flow.  
Phase 3 is the longer bulk run into the EC2 database.

---

## Main script

```bash
python scripts/04_generate_embeddings.py
```

This script:

1. Loads the local BioClinical embedding model
2. Finds rows with `clinical_embedding IS NULL`
3. Creates embeddings in batches
4. Saves them into the EC2 `patient_encounters` table

Current script idea:

- process in batches (example: `batch_size = 500`)
- stop after a limit (example: `demo_limit = 6000`)

You can change those numbers if your machine struggles.

---

## If your laptop cannot finish one long run

Local models can be heavy. Long runs may freeze, overheat, or get interrupted.

Safe approach:

1. Set a smaller limit (example: 2000)
2. Run the script
3. Wait until it finishes
4. Run the same script again

Why re-running works:

- each run only picks rows where `clinical_embedding IS NULL`
- already-filled rows are skipped
- so each run adds more vectors

Repeat until you have enough (for example ~10,000).  
On a normal laptop this can take a long time (often 1–2+ hours total).

---

## Playground file (learning only)

```bash
python scripts/04_embedder_playground.py
```

Use this to understand the model without touching the database.

- dry run only
- sample rows only
- no EC2 writes

Do real database filling with `04_generate_embeddings.py`.

---

## Verify embeddings were saved

After some runs, check how many vectors exist:

```bash
python scripts/02_verify_vector_ingestion.py
```

This counts rows where `clinical_embedding IS NOT NULL`.

You can also check in SQL on the EC2 database itself.

1. From your laptop, SSH into the instance. Use your `.pem` key and the Elastic IP saved as `DB_HOST` in `.env`:

```bash
ssh -i "your-key.pem" ubuntu@YOUR_ELASTIC_IP
```

2. Open `ehr_db` as the Postgres system user:

```bash
sudo -u postgres psql -d ehr_db
```

3. Count rows that already have an embedding:

```sql
SELECT COUNT(*) FROM patient_encounters WHERE clinical_embedding IS NOT NULL;
```

4. Optional checks while you are there:

```sql
-- rows still waiting for an embedding
SELECT COUNT(*) FROM patient_encounters WHERE clinical_embedding IS NULL;

-- confirm a filled row is 768 numbers
SELECT id, drug, vector_dims(clinical_embedding)
FROM patient_encounters
WHERE clinical_embedding IS NOT NULL
LIMIT 5;
```

5. Leave psql:

```text
\q
```

One-shot version (no interactive session):

```bash
sudo -u postgres psql -d ehr_db -c "SELECT COUNT(*) FROM patient_encounters WHERE clinical_embedding IS NOT NULL;"
```

Run this after a batch finishes. The number should go up each time you re-run `04_generate_embeddings.py`.

You can also prove the saved vectors are usable for search, not only that the column is filled:

```bash
python scripts/05_test_vector_search.py
```

This script:

1. Loads the same BioClinical model
2. Turns a sample medical sentence into a 768-number query vector
3. Searches `patient_encounters` on EC2 with pgvector cosine distance (`<=>`)
4. Prints the top 3 closest rows (diagnosis, drug, record id, distance)

It only reads the database. It does not insert or update rows.

A good result is three real clinical rows, with the closest match listed first (smallest distance). If the count above is still 0, this script has nothing to search.

---

## What “done” looks like for Phase 3

- Several thousand rows have embeddings
- Verify script shows a non-zero count
- `05_test_vector_search.py` returns nearby clinical rows
- You are ready for later search / RAG / guardrail work

---

## Common confusion

- High CPU usage can still happen even with GPU, because tokenization and Python overhead use CPU.
- First run is slowest because the model must load.
- Filling all rows is not required for learning/demo — a few thousand is usually enough.

---

## Phase 3 checklist

- [ ] Ran `04_generate_embeddings.py` at least once successfully
- [ ] Re-ran if needed until enough rows are filled
- [ ] Verified with `02_verify_vector_ingestion.py` (or SQL count)
- [ ] Ran `05_test_vector_search.py` and saw top matches
- [ ] Understood playground is practice-only (no DB writes)
