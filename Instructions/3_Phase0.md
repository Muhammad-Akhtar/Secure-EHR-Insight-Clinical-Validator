# Phase 0 — Setup AWS Database and Load EHR Data

Goal: put a PostgreSQL database on AWS EC2, then load the MIMIC clinical CSV into it from your laptop.

---

## 1. Download the EHR data

1. Download the dataset from Kaggle:  
   https://www.kaggle.com/datasets/isaacritharson/mimic-iv-cleaned-medical-transcripts
2. Put the CSV in the project `data/` folder.
3. The ingest script expects this exact file name:  
   `data/MIMIC_IV_Trasncript.csv`  
   (yes, the spelling is `Trasncript` — keep it matching the script)

---

## 2. Create an AWS EC2 instance

You need an AWS account.

### Security group (firewall)

Create a security group with inbound rules like:

| Type | Port | Source | Why |
|---|---:|---|---|
| SSH | 22 | My IP only | so you can log in |
| PostgreSQL | 5432 | My IP only | so your laptop can reach the DB |

Do **not** open PostgreSQL to the whole internet.

### EC2 size (enough for this phase)

- About **4 GB RAM**
- About **20 GB** storage  
  Why 20 GB? Ubuntu + PostgreSQL + packages need space.

Create the instance (Ubuntu is fine), attach the security group, and launch it.

### Elastic IP (fixed public IP)

Normal public IPs can change after stop/start.

1. Create an Elastic IP
2. Associate it with your EC2 instance
3. Save that IP — you will use it in `.env` as `DB_HOST`

---

## 3. Install PostgreSQL on EC2

Full install and remote-access steps are in:

- `instructions_notes_by_monal_sir/instructions.txt`
- `instructions_notes_by_monal_sir/AWS_EC2_Docker_Deployment_Guide.md` (later deployment notes)

In short, on EC2 you will:

1. Install PostgreSQL 14
2. Allow remote connections (`listen_addresses` + `pg_hba.conf`)
3. Create database: **`ehr_db`**
4. Create a DB user (example in notes: `fde_admin`)
5. Restart PostgreSQL

Database name used in this project: **`ehr_db`**  
(Not `hospital_db` — ignore that older name if you see it elsewhere.)

---

## 4. Connect from your laptop (`.env`)

In the project root, create a `.env` file (do not commit it):

```env
DB_USER=fde_admin
DB_PASSWORD=your_password
DB_HOST=your_elastic_ip
DB_PORT=5432
DB_NAME=ehr_db
```

Install Python packages if needed (from project requirements / notes), then run scripts from the project root.

---

## 5. Create schema and load data

What happens:

1. `scripts/01_ingest_baseline_data.py`
   - runs `src/database/schema.sql`
   - creates table `patient_encounters`
   - loads the CSV into that table
2. `scripts/02_verify_ingestion.py`
   - checks row count
   - prints a few sample rows

Run:

```bash
python scripts/01_ingest_baseline_data.py
python scripts/02_verify_ingestion.py
```

If verify shows rows and sample clinical fields, Phase 0 is done.

---

## Phase 0 checklist

- [ ] CSV is in `data/` with the expected file name
- [ ] EC2 is running with SSH + Postgres open to My IP
- [ ] Elastic IP is set and saved
- [ ] PostgreSQL installed, `ehr_db` created
- [ ] `.env` points to EC2
- [ ] `01_ingest_baseline_data.py` succeeded
- [ ] `02_verify_ingestion.py` shows data

Hopefully everything is completed.
