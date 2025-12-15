# CMSC 491 – HealthSymp

This project demonstrates the experimental setup designed to test factual grounding on chain-of-thought and unstructured prompts by comparing them to the 10 symptoms each query is referring to. These symptoms are represented by several Mayo Clinic sources which were manually extracted for the RAG pipeline.

* OpenAI embeddings
* ChromaDB
* Python virtual environments

It is designed to ingest `.txt` documents, chunk them, embed them, and query them using semantic similarity.

---

##  Prerequisites

Make sure you have the following installed:

* **Python 3.9+**
* **pip**
* **Git**

To check:

```bash
python --version
pip --version
git --version
```

---

## Environment Setup

### 1. Clone the repository

```bash
git clone https://github.com/jordanmaglalang/cmsc-491.git
cd cmsc-491
```

---

### 2. Create the virtual environment

```bash
python -m venv venv
```

Activate it:

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate.ps1
```

You should now see:

```
(venv)
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment Variables

This project uses an OpenAI API key stored in a `.env` file.

### 5. Create a `.env` file

```bash
touch .env
```

Add your API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

---



### 6.  Running the Project

Run the vector pipeline:

```bash
python vector.py
```

When prompted, enter the filename **without** `.txt`:

```text
Enter the filename (without .txt) to load text from: nausea
```

The script will:

* Load the document
* Chunk the text
* Embed the chunks
* Store them in ChromaDB
* Run example semantic queries

---

##  Project Structure

```
cmsc-491/
├── vector.py
├── requirements.txt
├── .gitignore
├── .env               
├── texts/
│   ├── nausea.txt
│   ├── back_soreness.txt
│   ├── dry_eyes.txt
│   ├── dry_mouth.txt
│   ├── feeling_warm.txt
│   ├── headache.txt
│   ├── light_cough.txt
│   ├── sore_throat.txt
│   ├── stuffy_nose.txt
│   └── upset_stomach.txt
├── venv/            
```



