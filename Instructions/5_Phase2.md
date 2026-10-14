# Phase 2 — Choose the Clinical Embedder and Fill Vectors

Goal: understand why we pick a medical embedding model, then start filling `clinical_embedding`.

---

## What we have after Phase 1

- Database with `pgvector` enabled
- Patient rows already loaded
- Column `clinical_embedding` exists, but most values are still empty (`NULL`)

---

## What we need to do

Take clinical text (admission type, drug, lab test, diagnosis, notes, etc.),  
convert it into a **768-number vector**,  
and save that vector into `clinical_embedding`.

Why? So later we can do **semantic search** (meaning-based search) with pgvector operators such as cosine similarity, directly inside PostgreSQL.

---

## Choosing the embedder

We should not pick a random general-purpose model.

Our data is clinical:

1. medicines / drugs
2. diseases / diagnoses
3. labs and hospital notes

A normal general text model may not understand medical wording well enough.

So we use a biomedical / clinical embedding model:

**`NeuML/bioclinical-modernbert-base-embeddings`**

Notes:

- This is an **embedding model** (turns text into vectors)
- It is **not** a chat LLM that answers questions
- Output size must be **768** to match `vector(768)`

---

## Script that does the real work

File: `scripts/04_generate_embeddings.py`

What it does:

1. Connects to AWS PostgreSQL using `.env`
2. Loads the BioClinical model (downloads once, then uses local Hugging Face cache)
3. Selects rows where `clinical_embedding IS NULL`
4. Builds one clinical text string per row
5. Encodes rows in batches
6. Updates `clinical_embedding` in the database

Important settings in the script:

- `batch_size` = how many rows encode/update together
- `demo_limit` = max rows to process in one run

You do **not** need to fill every row on day one.  
A few thousand embeddings is enough for demos.

---

## Helpful dry-run file (no database writes)

File: `scripts/04_embedder_playground.py`

Use this to learn:

- how the model loads
- how text is built
- how encoding works

It uses sample rows only. It does **not** write to the database.

---

## Practical tip

First model load is slow (download / cache / load into memory).  
Later runs are faster because the model is already cached on disk.

If CUDA GPU is available and PyTorch is the CUDA build, encoding can use GPU.  
Tokenization and DB updates still use CPU, so Task Manager may still show CPU activity.

---

## Phase 2 checklist

- [ ] You understand why a clinical embedder is needed
- [ ] Model name is `NeuML/bioclinical-modernbert-base-embeddings`
- [ ] Column size and model size both are 768
- [ ] You tried playground and/or started `04_generate_embeddings.py`
