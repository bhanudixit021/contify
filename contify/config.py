import os
from collections import defaultdict

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)  # Create the directory if it doesn't exist

# File paths
INVERTED_INDEX_PATH = os.path.join(DATA_DIR, "inverted_index.json")
DOCUMENTS_PATH = os.path.join(DATA_DIR, "documents.json")
DOCUMENT_FREQUENCIES_PATH = os.path.join(DATA_DIR, "document_frequencies.json")


INVERTED_INDEX = defaultdict(lambda: defaultdict(dict))
DOCUMENTS = {}
DOCUMENT_FREQUENCIES = defaultdict(int)  # Number of documents containing each term
TOTAL_DOCUMENTS = 0