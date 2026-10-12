
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = ROOT / "customer_shopping_behavior.csv"
SEGMENT_FILE = ROOT / "reports" / "customer_segments.csv"

st.set_page_config(
    page_title="Customer Insights | Analytics",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_csv(file_bytes):
    """Load a CSV dataset."""
    from io import BytesIO

    return pd.read_csv(BytesIO(file_bytes))


def load_default_data():
    if not DEFAULT_DATA.exists():
        return None

    return pd.read_csv(DEFAULT_DATA)


def money(value):
    return f"${value:,.2f}"


st.title("📊 Customer Shopping Analytics")
st.caption(
    "Interactive business intelligence dashboard "
    "for customer shopping behavior."
)

with st.sidebar:
    st.header("Data & Filters")

    uploaded_file = st.file_uploader(
        "Upload a customer CSV",
        type=["csv"],
    )

    if uploaded_file is not None:
        df = load_csv(uploaded_file.getvalue())
    else:
        df = load_default_data()

    if df is None:
        st.error("Upload a CSV file to begin.")
        st.stop()

    required = [
        "Customer ID",
        "Purchase Amount (USD)",
        "Category",
        "Season",
        "Gender",
        "Subscription Status",
        "Review Rating",
        "Item Purchased",
        "Discount Applied",
        "Previous Purchases",
    ]

    missing = sorted(set(required) - set(df.columns))

    if missing:
        st.error(
            "The dataset is missing required columns: "
            + ", ".join(missing)
        )
        st.stop()

    df = df.copy()

    numeric_columns = [
        "Customer ID",
        "Purchase Amount (USD)",
        "Review Rating",
        "Previous Purchases",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["Customer ID", "Purchase Amount (USD)"])

    categories = sorted(df["Category"].dropna().unique().tolist())
    seasons = sorted(df["Season"].dropna().unique().tolist())
    genders = sorted(df["Gender"].dropna().unique().tolist())
    subscriptions = sorted(
        df["Subscription Status"].dropna().unique().tolist()
    )

    selected_categories = st.multiselect(
        "Product category",
        categories,
        default=categories,
    )

    selected_seasons = st.multiselect(
        "Season",
        seasons,
        default=seasons,
    )

    selected_genders = st.multiselect(
        "Gender",
        genders,
        default=genders,
    )

    selected_subscriptions = st.multiselect(
        "Subscription status",
        subscriptions,
        default=subscriptions,
    )

filtered = df[
    df["Category"].isin(selected_categories)
    & df["Season"].isin(selected_seasons)
    & df["Gender"].isin(selected_genders)
    & df["Subscription Status"].isin(selected_subscriptions)
].copy()

if filtered.empty:
    st.warning("No records match your selected filters.")
    st.stop()

# KPI cards
total_customers = filtered["Customer ID"].nunique()
average_purchase = filtered["Purchase Amount (USD)"].mean()
total_purchase_amount = filtered["Purchase Amount (USD)"].sum()
average_rating = filtered["Review Rating"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Unique Customers", f"{total_customers:,}")
c2.metric("Average Purchase", money(average_purchase))
c3.metric("Total Purchase Amount", money(total_purchase_amount))
c4.metric(
    "Average Review Rating",
    f"{average_rating:.2f}" if pd.notna(average_rating) else "N/A",
)

st.divider()

# Purchase amount by category
left, right = st.columns(2)

with left:
    st.subheader("Purchase Amount by Category")

    category_data = (
        filtered.groupby("Category", as_index=False)
        .agg(
            total_amount=("Purchase Amount (USD)", "sum"),
            records=("Customer ID", "size"),
        )
        .sort_values("total_amount", ascending=False)
    )

    fig = px.bar(
        category_data,
        x="Category",
        y="total_amount",
        color="Category",
        hover_data=["records"],
        title="Total Purchase Amount",
        labels={
            "total_amount": "Purchase Amount (USD)",
            "Category": "Product Category",
        },
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Purchase Amount by Season")

    seasonal_data = (
        filtered.groupby("Season", as_index=False)
        .agg(
            total_amount=("Purchase Amount (USD)", "sum"),
        )
    )

    fig = px.bar(
        seasonal_data,
        x="Season",
        y="total_amount",
        color="Season",
        title="Seasonal Purchase Amount",
        labels={
            "total_amount": "Purchase Amount (USD)",
        },
    )

    st.plotly_chart(fig, use_container_width=True)

# Customer spending distribution
left, right = st.columns(2)

with left:
    st.subheader("Customer Purchase Distribution")

    fig = px.histogram(
        filtered,
        x="Purchase Amount (USD)",
        nbins=25,
        title="Distribution of Purchase Amounts",
        labels={
            "Purchase Amount (USD)": "Purchase Amount (USD)",
        },
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Spending by Gender")

    gender_data = (
        filtered.groupby("Gender", as_index=False)
        .agg(
            average_amount=("Purchase Amount (USD)", "mean"),
            records=("Customer ID", "size"),
        )
    )

    fig = px.bar(
        gender_data,
        x="Gender",
        y="average_amount",
        color="Gender",
        hover_data=["records"],
        title="Average Purchase Amount",
        labels={
            "average_amount": "Average Purchase Amount (USD)",
        },
    )

    st.plotly_chart(fig, use_container_width=True)

# Discount analysis
st.subheader("Discount Usage Analysis")

discount_data = (
    filtered.groupby("Discount Applied", as_index=False)
    .agg(
        average_amount=("Purchase Amount (USD)", "mean"),
        records=("Customer ID", "size"),
    )
)

fig = px.bar(
    discount_data,
    x="Discount Applied",
    y="average_amount",
    color="Discount Applied",
    hover_data=["records"],
    title="Average Purchase Amount by Discount Usage",
    labels={
        "Discount Applied": "Discount Applied",
        "average_amount": "Average Purchase Amount (USD)",
    },
)

st.plotly_chart(fig, use_container_width=True)

# Customer segmentation, when generated reports are available
st.subheader("Customer Behavioral Segments")

if SEGMENT_FILE.exists():
    segments = pd.read_csv(SEGMENT_FILE)

    if "Customer ID" in segments.columns and "customer_segment" in segments.columns:
        segment_data = segments[
            segments["Customer ID"].isin(filtered["Customer ID"])
        ]

        segment_counts = (
            segment_data.groupby("customer_segment")
            .size()
            .reset_index(name="customers")
            .sort_values("customers", ascending=False)
        )

        fig = px.bar(
            segment_counts,
            x="customer_segment",
            y="customers",
            color="customer_segment",
            title="Customer Segment Distribution",
            labels={
                "customer_segment": "Customer Segment",
                "customers": "Number of Customers",
            },
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("The segmentation report has an unexpected format.")
else:
    st.info(
        "Run python src/customer_segmentation.py "
        "to generate the customer segmentation report."
    )

# Detailed data explorer
st.subheader("Customer Data Explorer")

search = st.text_input(
    "Search item, category, or location",
    placeholder="Example: Jeans",
)

explorer_data = filtered.copy()

if search.strip():
    searchable_columns = [
        column
        for column in ["Item Purchased", "Category", "Location"]
        if column in explorer_data.columns
    ]

    mask = pd.Series(False, index=explorer_data.index)

    for column in searchable_columns:
        mask |= explorer_data[column].astype(str).str.contains(
            search.strip(),
            case=False,
            na=False,
            regex=False,
        )

    explorer_data = explorer_data[mask]

st.write(f"Showing {len(explorer_data):,} records")

st.dataframe(
    explorer_data,
    use_container_width=True,
    hide_index=True,
)

csv_data = explorer_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_customer_analysis.csv",
    mime="text/csv",
)

st.caption(
    "Note: The dataset does not include transaction dates or order IDs. "
    "Purchase amounts shown here describe the supplied records and "
    "should not be interpreted as verified lifetime or time-based revenue."
)

