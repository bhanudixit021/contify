import json
import os
import math
from typing import List
import config


def tokenize(text: str) -> List[str]:
    """Tokenize and normalize text."""
    return [word.lower().strip(".,!?") for word in text.split()]

def calculate_tf(term_count: int, total_terms: int) -> float:
    """Calculate Term Frequency (TF)."""
    return term_count / total_terms if total_terms > 0 else 0

def calculate_idf(total_documents: int, document_frequency: int) -> float:
    """Calculate Inverse Document Frequency (IDF)."""
    return math.log((total_documents + 1) / (document_frequency + 1)) + 1

def save_to_disk():
    """Save the inverted index and documents to disk."""
    with open(config.INVERTED_INDEX_PATH, "w") as f:
        json.dump(config.INVERTED_INDEX, f)
    with open(config.DOCUMENTS_PATH, "w") as f:
        json.dump(config.DOCUMENTS, f)
    with open(config.DOCUMENT_FREQUENCIES_PATH, "w") as f:
        json.dump(config.DOCUMENT_FREQUENCIES, f)

# def load_from_disk():
#     """Load the inverted index and documents from disk."""
#     if os.path.exists(config.INVERTED_INDEX_PATH):
#         with open(config.INVERTED_INDEX_PATH, "r") as f:
#             config.INVERTED_INDEX = json.load(f)
#     if os.path.exists(config.DOCUMENTS_PATH):
#         with open(config.DOCUMENTS_PATH, "r") as f:
#             config.DOCUMENTS = json.load(f)
#     if os.path.exists(config.DOCUMENT_FREQUENCIES_PATH):
#         with open(config.DOCUMENT_FREQUENCIES_PATH, "r") as f:
#             config.DOCUMENT_FREQUENCIES = json.load(f)
#     config.TOTAL_DOCUMENTS = len(config.DOCUMENTS)
from config import INVERTED_INDEX, DOCUMENTS, DOCUMENT_FREQUENCIES, TOTAL_DOCUMENTS, DOCUMENT_FREQUENCIES_PATH, DOCUMENTS_PATH, INVERTED_INDEX_PATH

def load_from_disk():
    global INVERTED_INDEX, DOCUMENTS, DOCUMENT_FREQUENCIES, TOTAL_DOCUMENTS

    try:
        with open(DOCUMENTS_PATH, "r") as f:
            DOCUMENTS.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        DOCUMENTS = {}

    try:
        with open(INVERTED_INDEX_PATH, "r") as f:
            INVERTED_INDEX.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        INVERTED_INDEX = {}

    try:
        with open(DOCUMENT_FREQUENCIES_PATH, "r") as f:
            DOCUMENT_FREQUENCIES.update(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        DOCUMENT_FREQUENCIES = {}

    TOTAL_DOCUMENTS = len(DOCUMENTS) 


def is_phrase_in_document(doc_id: str, phrase_terms: List[str]) -> bool:
    """Check if a phrase exists in a document."""
    if not phrase_terms:
        return False

    # Get positions of the first term in the phrase
    first_term = phrase_terms[0]
    if first_term not in config.INVERTED_INDEX or doc_id not in config.INVERTED_INDEX[first_term]:
        return False

    # Check positions of subsequent terms
    first_positions = config.INVERTED_INDEX[first_term][doc_id]["positions"]
    for i in range(1, len(phrase_terms)):
        term = phrase_terms[i]
        if term not in config.INVERTED_INDEX or doc_id not in config.INVERTED_INDEX[term]:
            return False

        # Check if the next term appears immediately after the previous term
        next_positions = config.INVERTED_INDEX[term][doc_id]["positions"]
        first_positions = [p + i for p in first_positions if (p + i) in next_positions]
        if not first_positions:
            return False

    return True