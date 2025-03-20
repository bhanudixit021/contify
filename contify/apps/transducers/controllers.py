from fastapi import APIRouter,HTTPException
from collections import defaultdict
from schemas import Document,SearchResponse
from helpers import tokenize,save_to_disk,is_phrase_in_document,calculate_idf,calculate_tf
from typing import List
from config import DOCUMENT_FREQUENCIES,DOCUMENTS,INVERTED_INDEX,TOTAL_DOCUMENTS



router = APIRouter(
    tags=["Index","Search"],
)

# inverted_index = defaultdict(lambda: defaultdict(dict))
# documents = {}
# document_frequencies = defaultdict(int)  # Number of documents containing each term
# total_documents = 0

@router.post("/index")
def index_document(doc: Document):
    """Index a document."""
    global INVERTED_INDEX,DOCUMENT_FREQUENCIES,DOCUMENTS, TOTAL_DOCUMENTS
    doc_id = doc.id
    title = doc.title
    data = doc.data

    # Tokenize and normalize text
    terms = tokenize(title) + tokenize(data)
    total_terms = len(terms)

    # Track unique terms in this document for document frequency
    unique_terms_in_doc = set()

    # Update inverted index
    for position, term in enumerate(terms):
        if doc_id not in INVERTED_INDEX[term]:
            INVERTED_INDEX[term][doc_id] = {"positions": [], "tf": 0}
        INVERTED_INDEX[term][doc_id]["positions"].append(position)
        INVERTED_INDEX[term][doc_id]["tf"] += 1

        # Track unique terms for document frequency
        unique_terms_in_doc.add(term)

    # Update document frequencies for IDF calculation
    for term in unique_terms_in_doc:
        DOCUMENT_FREQUENCIES[term] += 1

    # Store document
    DOCUMENTS[doc_id] = {"title": title, "data": data}
    TOTAL_DOCUMENTS += 1

    # Save to disk
    save_to_disk()

    return {"message": "Document indexed successfully"}



@router.get("/search")
def search(query: str) -> List[SearchResponse]:
    """Search for documents."""
    terms = tokenize(query)
    results = defaultdict(lambda: {"score": 0, "title": "", "data": ""})
    global INVERTED_INDEX,DOCUMENT_FREQUENCIES,DOCUMENTS, TOTAL_DOCUMENTS

    if len(terms) > 1:
        # Phrase query: Check if the entire phrase exists in documents
        for doc_id in DOCUMENTS:
            if is_phrase_in_document(doc_id, terms):
                # Calculate TF-IDF score for the phrase
                score = 0
                for term in terms:
                    if term in INVERTED_INDEX and doc_id in INVERTED_INDEX[term]:
                        idf = calculate_idf(TOTAL_DOCUMENTS, DOCUMENT_FREQUENCIES.get(term, 0))
                        tf = calculate_tf(INVERTED_INDEX[term][doc_id]["tf"], len(tokenize(DOCUMENTS[doc_id]["title"] + " " + DOCUMENTS[doc_id]["data"])))
                        score += tf * idf
                results[doc_id]["score"] = score
                results[doc_id]["title"] = DOCUMENTS[doc_id]["title"]
                results[doc_id]["data"] = DOCUMENTS[doc_id]["data"]
    else:
        # Normal query: Calculate TF-IDF scores for individual terms
        for term in terms:
            if term in INVERTED_INDEX:
                idf = calculate_idf(TOTAL_DOCUMENTS, DOCUMENT_FREQUENCIES.get(term, 0))
                for doc_id, details in INVERTED_INDEX[term].items():
                    tf = calculate_tf(details["tf"], len(tokenize(DOCUMENTS[doc_id]["title"] + " " + DOCUMENTS[doc_id]["data"])))
                    results[doc_id]["score"] += tf * idf
                    results[doc_id]["title"] = DOCUMENTS[doc_id]["title"]
                    results[doc_id]["data"] = DOCUMENTS[doc_id]["data"]

    # Ranking done by score
    ranked_results = sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)
    if not ranked_results:
        # Instead of returning a dictionary, raise an HTTPException with a message
        raise HTTPException(status_code=404, detail="No data matching the query was found")

    return [SearchResponse(id=doc_id, title=details["title"], data=details["data"], score=details["score"]) for doc_id, details in ranked_results]