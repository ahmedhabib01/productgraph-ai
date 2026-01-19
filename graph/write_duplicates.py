import os
import json
from neo4j import GraphDatabase
from enrichment.dedupe import find_duplicate_pairs

INPUT_PATH = "data_sources/_out_all_products_normalized.json"


def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def write_dupes(tx, pairs):
    # Remove old duplicate links (so reruns are clean)
    tx.run("MATCH (:Product)-[r:DUPLICATE_OF]->(:Product) DELETE r")

    for a, b, score in pairs:
        tx.run(
            """
            MATCH (p1:Product {id:$a})
            MATCH (p2:Product {id:$b})
            MERGE (p1)-[r:DUPLICATE_OF]->(p2)
            SET r.score = $score
            """,
            a=a,
            b=b,
            score=float(score),
        )


def main():
    uri = get_env("NEO4J_URI")
    user = get_env("NEO4J_USER")
    password = get_env("NEO4J_PASSWORD")

    products = json.load(open(INPUT_PATH, "r", encoding="utf-8"))
    pairs = find_duplicate_pairs(products, threshold=0.6)

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        session.execute_write(write_dupes, pairs)
    driver.close()

    print(f"Duplicate pairs found: {len(pairs)}")
    for a, b, s in pairs:
        print(f"- {a} ~ {b} (score={s:.2f})")


if __name__ == "__main__":
    main()