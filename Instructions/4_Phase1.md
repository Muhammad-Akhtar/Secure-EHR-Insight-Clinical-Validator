#### 1. Install pg_vector on aws

Install pg_vector
ubuntu@ip-172-31-34-127:~$ sudo apt install -y postgresql-14-pgvector


Verify the installation files
ubuntu@ip-172-31-34-127:~$ ls /usr/share/postgresql/14/extension/vector*


#### 2. Apply/Associate the pg vector extension to our ehr_db

Below command do this for us
```bash
sudo -u postgres psql -d ehr_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

- Now we have database with extension vector.

- `patient_encounters` is the database table.

- here we add a new columns in this table named `clinical_embeddings vector(768)`

- vector(768) is the data type of this column, like varchar(255)

- **768 sized vector** the llm that we are going to use extract embeddings of dimension of size 768.


- file to add new column inside ec2 instance database is inside scripts `03_...`

