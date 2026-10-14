# Phase 1 — Add pgvector and the Embedding Column

Goal: teach PostgreSQL how to store vectors, then add a vector column on `patient_encounters`.

At the end of Phase 0 you have normal table data.  
At the end of Phase 1 you can store 768-number embeddings next to each row.  
(The embeddings themselves are filled later in Phase 2 / Phase 3.)

---

## 1. Install pgvector on EC2

SSH into the EC2 instance, then install the extension package:

```bash
sudo apt update
sudo apt install -y postgresql-14-pgvector
```

Check the files are there:

```bash
ls /usr/share/postgresql/14/extension/vector*
```

You should see files like `vector.control` and `vector--...sql`.

---

## 2. Turn on the extension inside `ehr_db`

Installing the package is not enough. You must enable it in your database:

```bash
sudo -u postgres psql -d ehr_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

Now `ehr_db` understands the `vector` data type.

---

## 3. Add the embedding column

Table name: **`patient_encounters`**

New column name: **`clinical_embedding`**  
(Important: singular `embedding`, not `embeddings`)

Column type: **`vector(768)`**

What that means:

- each embedding is a list of **768 numbers**
- our clinical embedder model outputs size **768**
- database column size must match the model size

Run this from your laptop (project root):

```bash
python scripts/03_apply_vector_schema.py
```

That script runs something like:

```sql
ALTER TABLE patient_encounters
ADD COLUMN IF NOT EXISTS clinical_embedding vector(768);
```

If it prints that the column is confirmed, Phase 1 is done.

---

## What you have now

- PostgreSQL with `pgvector` enabled
- table `patient_encounters`
- column `clinical_embedding vector(768)` exists
- values are still mostly **NULL** (empty) until you generate embeddings

---

## Phase 1 checklist

- [ ] `postgresql-14-pgvector` installed on EC2
- [ ] `CREATE EXTENSION vector` ran on `ehr_db`
- [ ] `03_apply_vector_schema.py` succeeded
- [ ] column `clinical_embedding` exists
