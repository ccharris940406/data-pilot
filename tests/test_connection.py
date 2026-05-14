from dotenv import load_dotenv

_ = load_dotenv()
from app.services.embeddings import embeddings_service
from app.services.metadata_extractor import metadata_extractor

# Test 1: extraer schema
schema = metadata_extractor.extract()
print("=== SCHEMA ===")
for table, columns in schema.items():
    print(f"\n{table}:")
    for col in columns:
        print(f"  - {col['name']} ({col['type']})")

# Test 2: indexar en Chroma
print("\n=== INDEXING ===")
embeddings_service.index(schema)
print("Done!")

# Test 3: buscar
print("\n=== SEARCH ===")
results = embeddings_service.search("customers and their invoices")
for r in results:
    print(r)


from app.agents.nl2sql import nl2sql_agent

query = "How many artists are in the database?"
response = nl2sql_agent.run(query)
print(response)
