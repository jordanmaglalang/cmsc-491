# CMSC 491 – Vector Search & RAG Setup

This project demonstrates a basic **vector embedding and semantic search pipeline** using:

* OpenAI embeddings
* ChromaDB
* Python virtual environments

It is designed to ingest `.txt` documents, chunk them, embed them, and query them using semantic similarity.

---

## 📦 Prerequisites

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

## 🚀 Environment Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/cmsc-491.git
cd cmsc-491
```

---

### 2️⃣ Create a virtual environment

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

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

This project uses an OpenAI API key stored in a `.env` file.

### 4️⃣ Create a `.env` file

```bash
touch .env
```

Add your API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

⚠️ **Do not commit this file** — it is ignored via `.gitignore`.

---

## 📄 Text Data Setup

Create a folder for text documents:

```bash
mkdir texts
```

Add one or more `.txt` files:

```
texts/
 └── nausea.txt
```

Each file will be loaded, chunked, and embedded.

---

## ▶️ Running the Project

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

## 🧠 Project Structure

```
cmsc-491/
├── vector.py
├── requirements.txt
├── .gitignore
├── .env               # not committed
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
├── venv/              # not committed
```

---

## ⚠️ Security Notes

* Never hardcode API keys
* Never commit `.env`
* Rotate your OpenAI key if it was ever exposed

---

## 📚 Technologies Used

* Python
* OpenAI API
* ChromaDB
* NumPy
* python-dotenv

---

## 📌 Notes

This project is intended for educational purposes as part of **CMSC 491** and serves as a foundation for retrieval-augmented generation (RAG) systems.
