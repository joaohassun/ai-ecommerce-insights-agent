import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="AI E-commerce Insights Assistant",
    page_icon="🛒",
    layout="wide"
)

DATA_DIR = Path("data/raw")

@st.cache_data
def load_data():
    orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
    order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
    reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")
    products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"]
    )

    orders["order_delivered_customer_date"] = pd.to_datetime(
        orders["order_delivered_customer_date"],
        errors="coerce"
    )

    orders["order_estimated_delivery_date"] = pd.to_datetime(
        orders["order_estimated_delivery_date"],
        errors="coerce"
    )

    df = (
        orders
        .merge(order_items, on="order_id", how="left")
        .merge(reviews[["order_id", "review_score"]], on="order_id", how="left")
        .merge(products[["product_id", "product_category_name"]], on="product_id", how="left")
    )

    df["revenue"] = df["price"] + df["freight_value"]

    df["month"] = (
        df["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"]
        - df["order_estimated_delivery_date"]
    ).dt.days

    df["is_late"] = df["delivery_delay_days"] > 0

    return df

df = load_data()

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Overview Dashboard",
        "Customer Satisfaction",
        "Delivery Performance",
        "Business Recommendations",
        "Executive Report"
    ]
)

st.title("AI E-commerce Insights Assistant")

if page == "Overview Dashboard":

    st.header("Overview Dashboard")

    total_orders = df["order_id"].nunique()
    total_revenue = df["revenue"].sum()
    avg_review = df["review_score"].mean()
    late_rate = df["is_late"].mean() * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", f"{total_orders:,.0f}")
    col2.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
    col3.metric("Average Review", f"{avg_review:.2f}/5")
    col4.metric("Late Deliveries", f"{late_rate:.1f}%")

    st.subheader("Monthly Revenue")

    monthly_revenue = (
        df.groupby("month", as_index=False)["revenue"]
        .sum()
        .sort_values("month")
    )

    fig = px.line(
        monthly_revenue,
        x="month",
        y="revenue",
        title="Revenue Over Time"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Review Score Distribution")

    review_counts = (
        df["review_score"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    review_counts.columns = ["review_score", "count"]

    fig2 = px.bar(
        review_counts,
        x="review_score",
        y="count",
        title="Customer Review Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

elif page == "Customer Satisfaction":

    st.header("Customer Satisfaction Analysis")

    avg_review_late = (
        df.groupby("is_late")["review_score"]
        .mean()
        .reset_index()
    )

    avg_review_late["Delivery Status"] = avg_review_late["is_late"].map({
        False: "On Time",
        True: "Late"
    })

    fig = px.bar(
        avg_review_late,
        x="Delivery Status",
        y="review_score",
        title="Average Review Score by Delivery Status"
    )

    st.plotly_chart(fig, use_container_width=True)

    worst_categories = (
        df.groupby("product_category_name")["review_score"]
        .mean()
        .dropna()
        .sort_values()
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        worst_categories,
        x="review_score",
        y="product_category_name",
        orientation="h",
        title="Lowest Rated Product Categories"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "Late deliveries are associated with lower customer review scores, "
        "suggesting logistics performance is a key driver of satisfaction."
    )

elif page == "Delivery Performance":

    st.header("Delivery Performance")

    delivery_df = df.dropna(subset=["delivery_delay_days"])

    avg_delay = delivery_df["delivery_delay_days"].mean()
    late_rate = delivery_df["is_late"].mean() * 100

    col1, col2 = st.columns(2)

    col1.metric("Average Delay", f"{avg_delay:.1f} days")
    col2.metric("Late Deliveries", f"{late_rate:.1f}%")

    fig = px.histogram(
        delivery_df,
        x="delivery_delay_days",
        nbins=50,
        title="Delivery Delay Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

    late_categories = (
        delivery_df.groupby("product_category_name")["is_late"]
        .mean()
        .dropna()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    late_categories["late_rate"] = late_categories["is_late"] * 100

    fig2 = px.bar(
        late_categories,
        x="late_rate",
        y="product_category_name",
        orientation="h",
        title="Highest Late Delivery Categories"
    )

    st.plotly_chart(fig2, use_container_width=True)

elif page == "Business Recommendations":

    st.header("Business Recommendations")

    st.error(
        "HIGH PRIORITY: Reduce delivery delays for categories with the highest late delivery rates."
    )

    st.warning(
        "MEDIUM PRIORITY: Investigate low-rated categories and recurring customer dissatisfaction drivers."
    )

    st.info(
        "LOW PRIORITY: Continue monitoring revenue growth and customer satisfaction trends."
    )

elif page == "Executive Report":

    st.header("Automated Executive Report")

    total_orders = df["order_id"].nunique()
    total_revenue = df["revenue"].sum()
    avg_review = df["review_score"].mean()
    late_rate = df["is_late"].mean() * 100

    report = f'''
# Executive Summary

The business processed approximately {total_orders:,.0f} orders,
generating around R$ {total_revenue:,.0f} in revenue.

Average customer satisfaction was {avg_review:.2f}/5.

Late deliveries affected {late_rate:.1f}% of orders.

## Key Findings

- Delivery delays negatively impact review scores.
- Some product categories consistently underperform.
- Revenue growth accelerated significantly during 2017–2018.
- Logistics performance appears strongly linked to customer experience.

## Recommendations

- Improve logistics operations for high-delay categories.
- Monitor customer review trends continuously.
- Build operational dashboards for delivery risk tracking.
'''

    st.markdown(report)

    st.download_button(
        label="Download Executive Report",
        data=report,
        file_name="executive_report.md",
        mime="text/markdown"
    )