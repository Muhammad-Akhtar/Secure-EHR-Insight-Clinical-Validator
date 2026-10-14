#### We have

- Database with vector extions
- WE have data but clinical_embedding vector columns is empty

#### Doctor's comment

- convert into embedding and store into our column

- **Amazing thing about pg_vector is that we can do semantic search(cosine similarity) directly in postgresql with some operators**


#### Choosing Embedder.

- based upon data we choose embedder.
- what is special thing about our data?
- WE cannot choose a general embedder(transformer) because

1. Medicines
2. Drugs
3. disease

- does any general LLM(Transformer) have the super understanding of all above?
- NO. that's why we can't choose any LLM.

#### NeuM/Bioclinical text LLM/Transformer

- WE selected above llm. downloaded lcoallhy throguh scripts/04_generate_embedding.py file

- In batches and limit(demo_limit) it update the embedding vector column where it is null.

- 10 or 12 thousands embeddings are fine. As local modal is taking lot of time.

- Run the script to save few thousands embeddings. 