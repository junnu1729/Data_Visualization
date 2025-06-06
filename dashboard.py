import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="📊 Business Dashboard", layout="wide")

st.title("📈 Business Sales Dashboard")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Convert 'Date' column to datetime right after loading
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    st.sidebar.header("🔍 Filter Your Data")
    region_filter = st.sidebar.multiselect("Select Region", df["Region"].unique(), default=df["Region"].unique())
    category_filter = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())
    date_filter = st.sidebar.date_input("Select Date Range", [])

    filtered_df = df[
        (df["Region"].isin(region_filter)) &
        (df["Category"].isin(category_filter))
    ]

    if date_filter and len(date_filter) == 2:
        start, end = date_filter
        filtered_df = filtered_df[(filtered_df["Date"] >= pd.to_datetime(start)) & (filtered_df["Date"] <= pd.to_datetime(end))]

    st.subheader("📄 Data Preview")
    st.dataframe(filtered_df)

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Sales", f"₹{total_sales:,}")
    col2.metric("Total Profit", f"₹{total_profit:,}")

    st.markdown("---")

    fig1 = px.bar(filtered_df, x="Region", y="Sales", title="Sales by Region", color="Region")
    st.plotly_chart(fig1, use_container_width=True)

    # Make sure data is sorted by date before plotting
    filtered_df = filtered_df.sort_values("Date")
    fig2 = px.line(filtered_df, x="Date", y="Sales", color="Region", title="Sales Over Time")
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.pie(filtered_df, names="Category", values="Profit", title="Profit Distribution by Category")
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.box(filtered_df, x="Region", y="Profit", title="Profit Distribution by Region")
    st.plotly_chart(fig4, use_container_width=True)

    numeric_df = filtered_df.select_dtypes(include='number')
    if not numeric_df.empty:
        st.subheader("🔗 Correlation Heatmap")
        corr = numeric_df.corr(numeric_only=True)
        st.dataframe(corr.style.background_gradient(cmap="coolwarm"))

    st.download_button("📥 Download Filtered CSV", filtered_df.to_csv(index=False), file_name="filtered_data.csv")

else:
    st.info("📂 Please upload a CSV file to continue.")
