
from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "customer_shopping_behavior.csv"
SQL_FILE = PROJECT_ROOT / "customer_behavior_advanced_queries.sql"
DATABASE_FILE = PROJECT_ROOT / "customer_behavior.db"
OUTPUT_DIR = PROJECT_ROOT / "reports"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    if not SQL_FILE.exists():
        raise FileNotFoundError(f"SQL file not found: {SQL_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load the source CSV.
    df = pd.read_csv(DATA_FILE)

    # Create a local SQLite database and replace the analysis table.
    with sqlite3.connect(DATABASE_FILE) as connection:
        df.to_sql(
            "customer_shopping_behavior",
            connection,
            if_exists="replace",
            index=False,
        )

        sql_text = SQL_FILE.read_text(encoding="utf-8")

        # Each query in the SQL file is separated by a semicolon.
        queries = [
            query.strip()
            for query in sql_text.split(";")
            if query.strip()
        ]

        successful_queries = 0

        for number, query in enumerate(queries, start=1):
            result = pd.read_sql_query(query, connection)

            output_file = (
                OUTPUT_DIR / f"sql_analysis_{number:02d}.csv"
            )

            result.to_csv(output_file, index=False)

            print(f"\n{'=' * 60}")
            print(f"SQL ANALYSIS {number}")
            print("=" * 60)
            print(result.to_string(index=False))
            print(f"\nSaved: {output_file.name}")

            successful_queries += 1

    print("\n" + "=" * 60)
    print("SQL ANALYTICS COMPLETED")
    print("=" * 60)
    print(f"Queries executed: {successful_queries}")
    print(f"Database: {DATABASE_FILE}")
    print(f"Reports directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

