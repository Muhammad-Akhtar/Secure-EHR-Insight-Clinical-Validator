#### Running Script to save 10,000 embeddings into vector column of ec2

- It is quite a task, running local modal on my machine.
- It can't handle long running.
- Make batch size 500 and demo limit to 2000 it will insert those
- after updating 2000 run the scripts/04_generate_embedding.py again.
- repeat the process to complete 10,000. almost takes 2 hours on my local machine.

- Now we have inserted few record/embedding into our ec2 database.

### 04_embedder_playground.py (Understand)

- To understand how model is downloaded.
- how it works and interact with data.
- Dry run this file only. 