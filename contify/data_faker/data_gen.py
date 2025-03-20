import json
import random
from faker import Faker

# Initialize Faker for generating random text
fake = Faker()



import requests
import json
from time import sleep

url = "http://localhost:8000/index"

payload = json.dumps({
  "id": "1",
  "title": "quick fox",
  "data": "A fox is usually quick and brown."
})
headers = {
  'Content-Type': 'application/json',
  'x-api-key': '1234567',
  'Cookie': 'csrftoken=M5JHrqJ3yxnNVwx9gLeULl1qJdkuuZp9'
}




# Function to generate a random document
def generate_document(doc_id: int) -> dict:
    title = " ".join(fake.words(nb=random.randint(2, 5)))  # Random title with 2-5 words
    data = fake.paragraph(nb_sentences=random.randint(3, 7))  # Random paragraph with 3-7 sentences
    context = {
        "id": str(doc_id),
        "title": title,
        "data": data
    }
    payload = json.dumps(context)
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    sleep(0.1)
    
    return context

# Function to generate a dataset with millions of entries
def generate_dataset(num_documents: int, output_file: str):
    dataset = []
    for doc_id in range(1, num_documents + 1):
        document = generate_document(doc_id)
        dataset.append(document)
        if doc_id % 100000 == 0:  # Print progress every 100,000 documents
            print(f"Generated {doc_id} documents...")
    
    # Save the dataset to a JSON file
    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Dataset with {num_documents} documents saved to {output_file}")

# Generate a dataset with 1 million documents
generate_dataset(num_documents=1_000_000, output_file="dataset.json")