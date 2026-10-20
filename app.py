import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="DATAWISE | Air Quality",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 DATAWISE")
st.subheader("India Air Quality Intelligence")
st.write("Explore air-quality data through interactive charts.")

file = st.file_uploader(
    "Upload an air quality CSV dataset",
    type=["csv"]
)

if file is not None:
    df = pd.read_csv(file)

    st.success("Dataset loaded successfully!")
    st.write("Dataset preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("Dataset overview")
    c1, c2 = st.columns(2)
    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))

    st.subheader("Missing values")
    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Values"]
    st.dataframe(missing, use_container_width=True)

    numeric = df.select_dtypes(include="number").columns.tolist()

    if numeric:
        selected = st.selectbox(
            "Choose a measurement to analyze",
            numeric
        )

        chart_data = df[selected].dropna()

        if not chart_data.empty:
            fig = px.histogram(
                chart_data,
                x=selected,
                title=f"Distribution of {selected}"
            )
            st.plotly_chart(fig, use_container_width=True)

        if len(numeric) >= 2:
            x_col = st.selectbox("X-axis", numeric, index=0)
            y_col = st.selectbox("Y-axis", numeric, index=1)

            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col} vs {x_col}"
            )
            st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download cleaned dataset",
        df.dropna().to_csv(index=False),
        file_name="air_quality_cleaned.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a CSV file to begin exploring the data.")
    st.write("The dashboard will display dataset statistics, "
             "missing values, and interactive visualizations.")

st.caption(
    "DATAWISE | Data science educational project. "
    "Insights depend on the dataset supplied."
)
