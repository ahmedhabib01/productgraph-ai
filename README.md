# ProductGraph AI

A simple end-to-end project that shows how industrial product data can be collected from different sources, structured using a local LLM, and stored in a knowledge graph.

This project was built to demonstrate core skills needed for a **Founding Data Engineer** role.

---

## What this project does

- Ingests product data from:
  - A fake ERP API
  - XML files
  - Unstructured product datasheets
- Uses a **local LLM (Ollama)** to extract structured data from documents
- Normalizes and validates product data
- Detects duplicate products across sources
- Stores everything in a **Neo4j knowledge graph**
- Tracks basic data quality metrics

---

## Tech used

- Python
- FastAPI (mock ERP)
- Ollama (local LLM)
- Neo4j AuraDB Free
- GitHub Codespaces

All tools are free.

---

## Project structure

productgraph-ai/

  ├── api/
  
  ├── data_sources/ # XML, datasheets, outputs
  
  ├── ingestion/ # Data connectors
  
  ├── parsing/ # LLM parsing logic
  
  ├── enrichment/ # Normalization & deduplication
  
  ├── validation/ # Data quality checks
  
  ├── graph/ # Neo4j loaders
  
  ├── pipelines/ # Pipeline scripts
  
  ├── run_demo.sh # One-command demo
  
  └── README.md

---

## How to run the demo

### Requirements
- Neo4j AuraDB Free account
- Neo4j credentials set as Codespaces secrets:
  - `NEO4J_URI`
  - `NEO4J_USER`
  - `NEO4J_PASSWORD`
- Ollama running:
  ```bash
  ollama serve

Run everything
```bash
./run_demo.sh
````

## Example Neo4j Query

```cypher
MATCH (p:Product)-[:IN_CATEGORY]->(c:Category),
      (p)-[:MADE_BY]->(m:Manufacturer)
RETURN p.id, p.name, c.name AS category, m.name AS manufacturer;
```

## What the demo does

Running the demo will:

- Ingest data  
- Parse documents with an LLM  
- Normalize and validate data  
- Load data into Neo4j  
- Run deduplication  
- Show monitoring metrics  

