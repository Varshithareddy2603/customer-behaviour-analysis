
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "customer_shopping_behavior.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports"


def load_data():
    """Load and validate the customer dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)

    required_columns = [
        "Customer ID",
        "Purchase Amount (USD)",
        "Previous Purchases",
        "Subscription Status",
        "Discount Applied",
        "Review Rating",
        "Frequency of Purchases",
    ]

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    return df


def create_customer_segments(df):
    """Assign behavioral segments using transparent business rules."""
    df = df.copy()

    # Convert analytical columns to numeric values.
    numeric_columns = [
        "Purchase Amount (USD)",
        "Previous Purchases",
        "Review Rating",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Normalize text fields for consistent comparisons.
    for column in [
        "Subscription Status",
        "Discount Applied",
        "Frequency of Purchases",
    ]:
        df[column] = df[column].astype("string").str.strip().str.lower()

    # Calculate a customer-level profile.
    customer_profile = (
        df.groupby("Customer ID", as_index=False)
        .agg(
            avg_purchase_amount=("Purchase Amount (USD)", "mean"),
            previous_purchases=("Previous Purchases", "max"),
            avg_review_rating=("Review Rating", "mean"),
            subscription_status=("Subscription Status", "first"),
            discount_applied=("Discount Applied", "first"),
            purchase_frequency=("Frequency of Purchases", "first"),
            records=("Customer ID", "size"),
        )
    )

    # These are behavioral labels, not verified lifetime-value segments.
    def assign_segment(row):
        spending = row["avg_purchase_amount"]
        previous = row["previous_purchases"]
        frequency = row["purchase_frequency"]

        if pd.isna(spending) or pd.isna(previous):
            return "Insufficient Data"

        # Example thresholds for an initial, interpretable model.
        if spending >= 75 and previous >= 20:
            return "High-Spending Repeat Shoppers"

        if previous >= 20:
            return "Experienced Shoppers"

        if frequency in {"weekly", "fortnightly"}:
            return "Frequent-Shopping Pattern"

        if spending < 50:
            return "Lower-Spending Shoppers"

        return "General Shoppers"

    customer_profile["customer_segment"] = customer_profile.apply(
        assign_segment,
        axis=1,
    )

    return customer_profile


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = load_data()
    customer_profile = create_customer_segments(df)

    # Segment-level KPIs.
    segment_summary = (
        customer_profile.groupby("customer_segment", as_index=False)
        .agg(
            customers=("Customer ID", "nunique"),
            avg_purchase_amount=("avg_purchase_amount", "mean"),
            avg_previous_purchases=("previous_purchases", "mean"),
            avg_review_rating=("avg_review_rating", "mean"),
        )
        .sort_values("customers", ascending=False)
    )

    # Round numerical outputs for readability.
    numeric_columns = [
        "avg_purchase_amount",
        "avg_previous_purchases",
        "avg_review_rating",
    ]

    segment_summary[numeric_columns] = segment_summary[
        numeric_columns
    ].round(2)

    customer_profile.to_csv(
        OUTPUT_DIR / "customer_segments.csv",
        index=False,
    )

    segment_summary.to_csv(
        OUTPUT_DIR / "customer_segment_summary.csv",
        index=False,
    )

    print("\n" + "=" * 60)
    print("CUSTOMER BEHAVIORAL SEGMENTATION")
    print("=" * 60)

    print(f"Input records: {len(df):,}")
    print(f"Unique customer IDs: {df['Customer ID'].nunique():,}")
    print(f"Customer profiles: {len(customer_profile):,}")

    print("\nSEGMENT SUMMARY")
    print(segment_summary.to_string(index=False))

    print("\nFiles created:")
    print(OUTPUT_DIR / "customer_segments.csv")
    print(OUTPUT_DIR / "customer_segment_summary.csv")


if __name__ == "__main__":
    main()
