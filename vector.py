import os
from openai import OpenAI
import chromadb
from chromadb.utils import embedding_functions
import numpy as np
import re
from dotenv import load_dotenv
import os
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



# Loading the text file of a symptom document
def load_text_file(filename, folder="texts"):
   
    if not filename.endswith(".txt"):
        filename += ".txt"

    file_path = os.path.join(folder, filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Text file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

  
    text = re.sub(r'\n{3,}', '\n\n', text)  
    text = text.strip()

    return text
# Chunk the source into shorter sentences
def chunk_text_sentences(text, max_sentences=5, overlap=1):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = " ".join(sentences[i:i+max_sentences])
        chunks.append(chunk)
        i += max_sentences - overlap
    return chunks

# Process and validate each chunk
def validate_chunk(chunk, max_chars=30000):
   
  
    if not chunk or not isinstance(chunk, str):
        print(f"Invalid chunk type: {type(chunk)}")
        return False, None
    
  
    cleaned = chunk.strip()
    
    
    if not cleaned:
        print("Empty chunk after stripping whitespace")
        return False, None
    
    if len(cleaned) > max_chars:
        print(f"Warning: Chunk too long ({len(cleaned)} chars), truncating to {max_chars}")
        cleaned = cleaned[:max_chars]
    
    return True, cleaned
# Similarity conversion
def distance_to_similarity(distances):
    sims = [1 - (d / 2) for d in distances]
    return [max(0.0, min(1.0, s)) for s in sims]



# Input text filename

data = input("Enter the filename (without .txt) to load text from: ")
text = load_text_file(data) 
print(text)


chunks = chunk_text_sentences(text)
print(f"Text split into {len(chunks)} chunks.")

# Filter and validate chunks
valid_chunks = []
valid_ids = []
valid_metadatas = []

for i, chunk in enumerate(chunks):
    is_valid, cleaned_chunk = validate_chunk(chunk)
    if is_valid:
        valid_chunks.append(cleaned_chunk)
        valid_ids.append(f"chunk_{i}")
        valid_metadatas.append({"source": "example_text"})
    else:
        print(f"Skipping invalid chunk {i}")

print(f"Valid chunks: {len(valid_chunks)} out of {len(chunks)}")

# Initialize ChromaDB client and collection
chroma_client = chromadb.Client()

collection = chromadb.Client().get_or_create_collection(
    name="symptom_docs",
    metadata={"metric": "cosine"},
    embedding_function=embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )
)

# Add valid chunks to collection
if valid_chunks:
    try:
        collection.add(
            ids=valid_ids,
            documents=valid_chunks,
            metadatas=valid_metadatas
        )
        print(f"Successfully added {len(valid_chunks)} chunks to collection")
    except Exception as e:
        print(f"Error adding chunks to collection: {e}")
        print("Attempting to add chunks individually...")
        
        # Fallback: add chunks one by one
        for i, (chunk_id, doc, meta) in enumerate(zip(valid_ids, valid_chunks, valid_metadatas)):
            try:
                collection.add(
                    ids=[chunk_id],
                    documents=[doc],
                    metadatas=[meta]
                )
                print(f"Successfully added chunk {i}")
            except Exception as e2:
                print(f"Failed to add chunk {i}: {e2}")
                print(f"Chunk preview: {doc[:100]}...")
else:
    print("No valid chunks to add to collection")


queries = [
    "I'm sorry to hear that you're feeling nauseous after eating fast. It's common to feel this way when we eat too quickly. Maybe try sitting down, taking deep breaths, and drinking some water to help settle your stomach. If the nausea persists or worsens, it might be a good idea to consult a healthcare professional. Take care!",
 """ I considered the sudden onset of slight nausea after fast food consumption, potential causes related to food quality or quantity, and the need to assess for any concerning symptoms or patterns. It's important to note the duration and severity of your nausea. Could you describe how long it lasts and if there are any other symptoms present? After eating fast food, nausea could be due to the richness or greasiness of the food, food poisoning, or indigestion. For now, try resting and drinking water. If the nausea worsens, persists, or is accompanied by severe symptoms like vomiting or abdominal pain, it would be wise to seek medical advice. Remember, this guidance is not a substitute for professional medical consultation.

"""
]

# Query the collection
for q_idx, query_text in enumerate(queries, 1):

    is_valid, cleaned_query = validate_chunk(query_text)
    
    if not is_valid:
        print(f"\nSkipping invalid query {q_idx}")
        continue
    
    try:
        results = collection.query(
            query_texts=[cleaned_query],
            n_results=3
        )

        similarities = distance_to_similarity(results['distances'][0])
        documents = results['documents'][0]

        sorted_docs = sorted(
            zip(similarities, documents),
            key=lambda x: x[0],
            reverse=True
        )

        print(f"\nTop matches for query {q_idx} --> {query_text} : ")
        for sim, doc in sorted_docs:
            print(f"Similarity: {sim:.3f}\nText: {doc}\n")
    except Exception as e:
        print(f"Error querying with query {q_idx}: {e}")
