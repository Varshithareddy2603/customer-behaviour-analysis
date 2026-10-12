
from pathlib import Path

import numpy as np
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "customer_shopping_behavior.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports"


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the customer shopping dataset."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError("The dataset is empty.")

    # Remove accidental whitespace from column names.
    df.columns = df.columns.str.strip()

    return df


def build_column_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a data quality report for every column."""
    report = pd.DataFrame({
        "column": df.columns,
        "data_type": [str(df[col].dtype) for col in df.columns],
        "missing_count": [int(df[col].isna().sum()) for col in df.columns],
        "missing_percentage": [
            round(df[col].isna().mean() * 100, 2)
            for col in df.columns
        ],
        "unique_values": [int(df[col].nunique(dropna=True)) for col in df.columns],
        "duplicate_values": [
            int(df[col].duplicated().sum()) for col in df.columns
        ],
    })

    return report


def check_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Check selected business rules supported by the dataset."""
    issues = []

    def add_issue(rule, count, details):
        issues.append({
            "rule": rule,
            "issue_count": int(count),
            "details": details,
        })

    # Customer ID should not be missing.
    if "Customer ID" in df.columns:
        count = df["Customer ID"].isna().sum()
        add_issue(
            "Missing customer IDs",
            count,
            "Customer IDs should be present.",
        )

        customer_ids = pd.to_numeric(df["Customer ID"], errors="coerce")
        invalid_ids = customer_ids.isna() | (customer_ids <= 0)

        add_issue(
            "Invalid customer IDs",
            invalid_ids.sum(),
            "Customer IDs should be positive numeric values.",
        )

        add_issue(
            "Repeated customer IDs",
            df["Customer ID"].duplicated(keep=False).sum(),
            "Review repeated IDs before treating records as individual customers.",
        )

    # Review ratings are expected to be between 1 and 5.
    if "Review Rating" in df.columns:
        ratings = pd.to_numeric(df["Review Rating"], errors="coerce")
        invalid_ratings = ratings.notna() & ~ratings.between(1, 5)

        add_issue(
            "Review ratings outside 1-5",
            invalid_ratings.sum(),
            "Review ratings should be between 1 and 5.",
        )

        add_issue(
            "Unparseable review ratings",
            (df["Review Rating"].notna() & ratings.isna()).sum(),
            "Review ratings should be numeric.",
        )

    # Purchase amounts should not be negative.
    if "Purchase Amount (USD)" in df.columns:
        amounts = pd.to_numeric(
            df["Purchase Amount (USD)"], errors="coerce"
        )

        add_issue(
            "Negative purchase amounts",
            (amounts < 0).sum(),
            "Review negative purchase amounts.",
        )

        add_issue(
            "Unparseable purchase amounts",
            (df["Purchase Amount (USD)"].notna() & amounts.isna()).sum(),
            "Purchase amounts should be numeric.",
        )

    # Ages should be positive.
    if "Age" in df.columns:
        ages = pd.to_numeric(df["Age"], errors="coerce")

        add_issue(
            "Invalid ages",
            (ages.notna() & ((ages <= 0) | (ages > 120))).sum(),
            "Review ages outside the range 1-120.",
        )

        add_issue(
            "Unparseable ages",
            (df["Age"].notna() & ages.isna()).sum(),
            "Age values should be numeric.",
        )

    # Previous purchases should be non-negative.
    if "Previous Purchases" in df.columns:
        previous = pd.to_numeric(
            df["Previous Purchases"], errors="coerce"
        )

        add_issue(
            "Invalid previous purchase counts",
            (previous.notna() & (previous < 0)).sum(),
            "Previous purchase counts should not be negative.",
        )

        add_issue(
            "Unparseable previous purchase counts",
            (df["Previous Purchases"].notna() & previous.isna()).sum(),
            "Previous purchase counts should be numeric.",
        )

    return pd.DataFrame(
        issues,
        columns=["rule", "issue_count", "details"],
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data(DATA_FILE)

    column_report = build_column_report(df)
    business_rules = check_business_rules(df)

    # Overall dataset summary.
    summary = pd.DataFrame([{
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "duplicate_rows": int(df.duplicated().sum()),
        "total_missing_values": int(df.isna().sum().sum()),
        "columns_with_missing_values": int(
            (df.isna().sum() > 0).sum()
        ),
        "numeric_columns": int(
            len(df.select_dtypes(include=np.number).columns)
        ),
        "categorical_columns": int(
            len(df.select_dtypes(include=["object", "category"]).columns)
        ),
    }])

    # Numerical descriptive statistics.
    numeric_summary = df.describe(include=[np.number]).T
    numeric_summary.index.name = "column"
    numeric_summary = numeric_summary.reset_index()

    # Export reports.
    summary.to_csv(OUTPUT_DIR / "dataset_summary.csv", index=False)
    column_report.to_csv(OUTPUT_DIR / "column_quality_report.csv", index=False)
    business_rules.to_csv(OUTPUT_DIR / "business_rule_issues.csv", index=False)
    numeric_summary.to_csv(OUTPUT_DIR / "numeric_summary.csv", index=False)

    print("\n" + "=" * 55)
    print("CUSTOMER SHOPPING DATA QUALITY REPORT")
    print("=" * 55)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")
    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print(f"Missing values: {df.isna().sum().sum():,}")

    print("\nCOLUMN QUALITY")
    print(column_report.to_string(index=False))

    print("\nBUSINESS RULE CHECKS")
    print(business_rules.to_string(index=False))

    print(f"\nReports saved to: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
