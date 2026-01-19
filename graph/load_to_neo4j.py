import os
import json
from neo4j import GraphDatabase

INPUT_PATH = "data_sources/_out_all_products_normalized.json"


def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def create_constraints(tx):
    tx.run(
        "CREATE CONSTRAINT product_id IF NOT EXISTS "
        "FOR (p:Product) REQUIRE p.id IS UNIQUE"
    )
    tx.run(
        "CREATE CONSTRAINT category_name IF NOT EXISTS "
        "FOR (c:Category) REQUIRE c.name IS UNIQUE"
    )
    tx.run(
        "CREATE CONSTRAINT manufacturer_name IF NOT EXISTS "
        "FOR (m:Manufacturer) REQUIRE m.name IS UNIQUE"
    )
    tx.run(
        "CREATE CONSTRAINT speckey_name IF NOT EXISTS "
        "FOR (s:SpecKey) REQUIRE s.name IS UNIQUE"
    )


def load_products(tx, products):
    for p in products:
        tx.run(
            """
            MERGE (prod:Product {id: $id})
            SET prod.name = $name,
                prod.source = $source
            MERGE (cat:Category {name: $category})
            MERGE (man:Manufacturer {name: $manufacturer})
            MERGE (prod)-[:IN_CATEGORY]->(cat)
            MERGE (prod)-[:MADE_BY]->(man)
            """,
            id=p["id"],
            name=p["name"],
            source=p.get("source", "unknown"),
            category=p.get("category", "Unknown"),
            manufacturer=p.get("manufacturer", "Unknown"),
        )

        specs = p.get("specs", {})
        if not isinstance(specs, dict):
            continue

        for k, v in specs.items():
            tx.run(
                """
                MATCH (prod:Product {id: $id})
                MERGE (sk:SpecKey {name: $key})
                MERGE (prod)-[r:HAS_SPEC]->(sk)
                SET r.value_str = $value
                """,
                id=p["id"],
                key=str(k),
                value=str(v),
            )



def main():
    uri = get_env("NEO4J_URI")
    user = get_env("NEO4J_USER")
    password = get_env("NEO4J_PASSWORD")

    products = json.load(open(INPUT_PATH, "r", encoding="utf-8"))

    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        # 1️⃣ Schema first
        session.execute_write(create_constraints)
        # 2️⃣ Data second
        session.execute_write(load_products, products)

    driver.close()
    print(f"Loaded {len(products)} products into Neo4j.")


if __name__ == "__main__":
    main()