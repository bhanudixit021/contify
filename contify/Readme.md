# Search Engine API

A simple search engine API built with FastAPI that supports indexing and searching documents using an inverted index and TF-IDF scoring.

## Features
- Index documents with a title and content.
- Search using individual terms or phrase queries.
- Persistent storage of indexed data.
- Ranked search results based on TF-IDF scores.

---

## 📌 Setup
### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Run the FastAPI Application**
```bash
uvicorn main:app --reload
```
By default, the API will be available at: **http://127.0.0.1:8000**

---

## 📂 Directory Structure
```
.
├── Makefile                    # Basic commands setup
├── Readme.md                   # Project documentation 
├── apps                       
│   └── transducers             
│       └── controllers.py      # api routers
├── config.py                   # Configuration settings
├── data
│   ├── document_frequencies.json # Term frequencies
│   ├── documents.json          # Stored documents
│   └── inverted_index.json     # Inverted index data
├── data_faker
│   └── data_gen.py             # random data generator
├── helpers.py                  # Helper function
├── main.py                     # project entry point
└── schemas.py                  # fastapi model schemas 

```

---

## 📌 API Endpoints

### **Index a Document**
#### **Endpoint:**
```http
POST /index
```
#### **Request Body:**
```json
{
    "id": "doc1",
    "title": "Introduction to FastAPI",
    "data": "FastAPI is a modern web framework for building APIs with Python."
}
```
#### **Response:**
```json
{
    "message": "Document indexed successfully"
}
```

---

### **Search for Documents**
#### **Endpoint:**
```http
GET /search?query=<search_term>
```
#### **Example Request (cURL):**
```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/search?query=fastapi' \
  -H 'accept: application/json'
```
#### **Example Response:**
```json
[
    {
        "id": "doc1",
        "title": "Introduction to FastAPI",
        "data": "FastAPI is a modern web framework for building APIs with Python.",
        "score": 1.2345
    }
]
```
#### **No Results Found Response:**
```json
{
    "detail": "No data matching the query was found"
}
```

---


## 🛠 Troubleshooting
- If documents are not being indexed, check if the **data/** directory is writable.
- If the search is returning no results, verify that documents exist in **data/documents.json**.
- If API responses seem incorrect, try deleting the **data/** directory and restarting the app.

---

## 📜 License
This project is open-source and available under the **MIT License**.

