#!/usr/bin/env bash
set -e

echo "-> Ingestion"
python -m pipelines.run_ingestion

echo "-> Parsing (LLM)"
python -m pipelines.run_parsing

echo "-> Enrichment"
python -m pipelines.run_enrichment

echo "-> Validation"
python -m pipelines.run_validation

echo "-> Load to Neo4j"
python -m graph.load_to_neo4j

echo "-> Deduplication"
python -m graph.write_duplicates

echo "-> Monitoring"
python -m pipelines.run_monitoring

echo "✅ Demo completed successfully"
