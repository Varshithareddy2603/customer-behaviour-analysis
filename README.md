# Customer Behaviour Analysis

An end-to-end data analytics project exploring customer shopping behaviour using Python, SQL, Streamlit, Plotly, and Power BI.

## 📌 Project Overview

This project analyses a customer shopping dataset containing 3,900 records and 18 columns to explore purchase amounts, product categories, seasons, discounts, subscriptions, shopping frequency, and customer ratings.

The goal is to turn raw customer data into meaningful business insights using data analysis, SQL queries, customer segmentation, and interactive visualisations.

## 🚀 Features

### 1. Interactive Streamlit Dashboard

* Interactive filters for category, season, gender, and subscription status.
* KPI cards for customer count, average purchase amount, total recorded purchase amount, and average review rating.
* Interactive charts for category performance, seasonal purchasing, purchase distributions, gender comparisons, and discount usage.
* Searchable data table and filtered-data download.

### 2. Data Quality Analysis

* Identifies missing values and duplicate records.
* Summarises column data types and numerical statistics.
* Checks business rules such as valid review ratings, non-negative purchase amounts, valid ages, and previous purchase counts.
* Exports data quality reports as CSV files.

### 3. Customer Segmentation

* Builds customer profiles using purchase amount, previous purchases, ratings, subscription status, and shopping frequency.
* Assigns rule-based customer segments.
* Generates customer-level segment data and segment summaries.

**Note:** These are predefined rule-based groups, not results from a trained clustering model or validated predictions.

### 4. SQL Business Analytics

SQL queries analyse:

* Overall shopping metrics.
* Purchase amounts by product category.
* Subscription behaviour.
* Discount and promotional code usage.
* Shopping frequency.
* Seasonal category performance.
* Spending groups.
* Review ratings by category.
* Payment methods.

### 5. Power BI Dashboard

The repository includes a Power BI dashboard file for interactive business reporting and visual analysis.

## 🛠️ Technology Stack

* **Python** — Data processing and analysis
* **Pandas and NumPy** — Data manipulation
* **SQLite and SQL** — Database queries and business analytics
* **Streamlit** — Interactive web dashboard
* **Plotly** — Interactive visualisations
* **Power BI** — Business intelligence and reporting
* **Git and GitHub** — Version control

## 📂 Project Structure

```text
customer-behaviour-analysis/
│
├── src/
│   ├── dashboard.py
│   ├── data_quality_report.py
│   ├── customer_segmentation.py
│   └── run_sql_analytics.py
│
├── reports/
│   ├── dataset_summary.csv
│   ├── column_quality_report.csv
│   ├── business_rule_issues.csv
│   ├── numeric_summary.csv
│   ├── customer_segments.csv
│   └── customer_segment_summary.csv
│
├── customer_behavior_advanced_queries.sql
├── customer_shopping_behavior.csv
├── Customer_Shopping_Behavior_Analysis.ipynb
├── customer_behavior_dashboard.pbix
├── requirements.txt
├── .gitignore
└── README.md
```

The repository may also contain the original project documents and supporting files.

## 📊 Dataset Description

The dataset contains **3,900 records and 18 columns**, including:

* Customer ID
* Age and gender
* Item purchased and product category
* Purchase amount
* Location, size, colour, and season
* Review rating
* Subscription status
* Shipping type
* Discount and promotional code usage
* Previous purchases
* Payment method
* Frequency of purchases

The review rating column contains 37 missing values. The data quality report identifies these missing values rather than treating them as valid ratings.

## 💻 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Varshithareddy2603/customer-behaviour-analysis.git
```

### 2. Navigate to the project directory

```bash
cd customer-behaviour-analysis
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the interactive dashboard

```bash
python -m streamlit run src/dashboard.py
```

Open the local URL displayed in your terminal to access the dashboard.

### 5. Generate data quality reports

```bash
python src/data_quality_report.py
```

### 6. Generate customer segments

```bash
python src/customer_segmentation.py
```

### 7. Run SQL analytics

```bash
python src/run_sql_analytics.py
```

Generated reports are saved in the `reports/` directory.

## 📈 Key Business Insights

The initial analysis identified the following patterns:

* **3,900 customer records** and 3,900 unique customer IDs.
* **$59.76** average recorded purchase amount.
* **$233,081** sum of recorded purchase amounts.
* **Clothing** has the highest number of records among the product categories.
* **Footwear** has the highest average review rating among the listed categories.

These findings are descriptive and based on the supplied dataset. The dataset does not contain transaction dates or order IDs, so this project does not claim time-based revenue trends or customer lifetime value.

## 🔮 Future Improvements

* Deploy the Streamlit dashboard online and add a live demo link.
* Add automated tests for data validation and analytics.
* Evaluate customer segments against defined business objectives.
* Expand exploratory data analysis and statistical testing.
* Add dashboard screenshots and a documented insights section.
* Automate data profiling for uploaded datasets.

## 👩‍💻 Author

**Varshitha Reddy Mothe**

* **GitHub Profile:** https://github.com/Varshithareddy2603
* **Project Repository:** https://github.com/Varshithareddy2603/customer-behaviour-analysis
