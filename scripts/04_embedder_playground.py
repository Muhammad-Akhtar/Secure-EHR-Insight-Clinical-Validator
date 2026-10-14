import torch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Sample rows shaped like patient_encounters mappings (no DB).
# Add more rows here to exercise larger batches / demo_limit.
SAMPLE_ROWS = [
    {
        "id": 1,
        "admission_type": "EMERGENCY",
        "drug": "Metformin",
        "test_name": "HbA1c",
        "drg_severity": "Moderate",
        "description": "Type 2 diabetes mellitus",
        "comments": "Patient reports polyuria and fatigue.",
    },
    {
        "id": 2,
        "admission_type": "ELECTIVE",
        "drug": "Lisinopril",
        "test_name": "BNP",
        "drg_severity": "Major",
        "description": "Congestive heart failure",
        "comments": "Stable on current regimen; follow-up in 2 weeks.",
    },
    {
        "id": 3,
        "admission_type": "URGENT",
        "drug": "Amoxicillin",
        "test_name": "CBC",
        "drg_severity": "Minor",
        "description": "Community-acquired pneumonia",
        "comments": "Started antibiotics; oxygen saturation improving.",
    },
]


def generate_embeddings_playground():
    # Prefer GPU when CUDA is available; otherwise fall back to CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        print(f"🚀 CUDA available — using GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️ CUDA not available — using CPU")

    model = None
    try:
        # 1. Load the BioClinical ModernBERT embedding model
        print("⏳ Loading local BioClinical ModernBERT model...")
        model = SentenceTransformer('NeuML/bioclinical-modernbert-base-embeddings')
        print(f"📍 Model device: {model.device}")

        # Guardrail: Programmatically verify the output dimension is 768
        if model.get_sentence_embedding_dimension() != 768:
            raise ValueError("CRITICAL DIMENSION MISMATCH: Model output does not match database vector(768).")

        # Increase batch size for network efficiency
        batch_size = 1
        # For a demo, 10,000 records is perfect to prove scale without waiting hours
        demo_limit = 3

        print(f"🚀 Generating batched embeddings for up to {demo_limit} patient records...")

        # In-memory stand-in for rows with clinical_embedding IS NULL
        pending = list(SAMPLE_ROWS)
        offset = 0

        with tqdm(total=demo_limit, desc="Vectorizing PHI", unit="rows") as pbar:
            processed = 0

            while processed < demo_limit:
                # Fetch a batch of records
                batch = pending[offset:offset + batch_size]

                if not batch:
                    break # No more NULL records

                # 1. Extract strings into a single list for parallel processing
                clinical_texts = []
                ids = []
                for row in batch:
                    components = []
                    if row['admission_type']: components.append(f"Admission: {row['admission_type']}")
                    if row['drug']: components.append(f"Prescribed: {row['drug']}")
                    if row['test_name']: components.append(f"Lab Test: {row['test_name']}")
                    if row['drg_severity']: components.append(f"Severity Level: {row['drg_severity']}")
                    if row['description']: components.append(f"Diagnosis: {row['description']}")
                    if row['comments']: components.append(f"Notes: {row['comments'][:250]}")

                    clinical_texts.append(" | ".join(components))
                    ids.append(row['id'])

                # 2. BATCHED ENCODING: Feed the entire list to the model at once!
                # Force the same device; keep tensors on GPU until we convert for inspect/update.
                emb_tensors = model.encode(
                    clinical_texts,
                    batch_size=batch_size,
                    device=device,
                    convert_to_tensor=True,
                )
                if device == "cuda":
                    torch.cuda.synchronize()
                    print(
                        f"  GPU confirm: emb.device={emb_tensors.device}, "
                        f"vram_MB={torch.cuda.memory_allocated() / 1024**2:.1f}"
                    )
                embeddings = emb_tensors.detach().cpu().tolist()

                # 3. Prepare BULK update parameters
                update_params = [
                    {"id": record_id, "embedding": str(emb)}
                    for record_id, emb in zip(ids, embeddings)
                ]

                # (DB bulk update omitted — inspect / play with results here)
                print(f"\nBatch @ processed={processed}: {len(update_params)} embeddings ready")
                print(f"  sample text: {clinical_texts[0][:120]}...")
                print(f"  embedding dim: {len(embeddings[0])}, id={update_params[0]['id']}")

                offset += len(batch)
                processed += len(batch)
                pbar.update(len(batch))

        print("\n✅ Playground complete: embeddings generated (not written to DB).")
    finally:
        # Release model / CUDA so this process does not keep holding GPU/CPU after finish
        if model is not None:
            del model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()


if __name__ == "__main__":
    generate_embeddings_playground()
