import os
from neo4j import GraphDatabase


def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def main():
    uri = get_env("NEO4J_URI")
    user = get_env("NEO4J_USER")
    password = get_env("NEO4J_PASSWORD")

    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        result = session.run("RETURN 1 AS ok")
        print("Neo4j test result:", result.single()["ok"])

    driver.close()
    print("✅ Successfully connected to Neo4j")


if __name__ == "__main__":
    main()