import streamlit as st
import requests
import pandas as pd

# -----------------------------
# CONFIG (Updated with your new key)
# -----------------------------
DEFAULT_API_KEY = "579b464db66ec23bdd000001a91006a69a344a2f5750f6bda75532d8"
DEFAULT_API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Data.gov.in API Tester", layout="wide")
st.title("🔍 Data.gov.in API Key Tester Dashboard")

st.markdown("Test your Data.gov.in API key and visualize response data instantly.")

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("API Configuration")

api_key = st.sidebar.text_input("API Key", value=DEFAULT_API_KEY, type="password")
api_url = st.sidebar.text_input("API URL", value=DEFAULT_API_URL)
limit = st.sidebar.slider("Limit Records", min_value=1, max_value=1000, value=25)

fetch_button = st.sidebar.button("🚀 Fetch Data")

# -----------------------------
# FETCH FUNCTION
# -----------------------------
def fetch_data(api_url, api_key, limit):
    params = {
        "api-key": api_key,
        "format": "json",
        "limit": limit
    }

    try:
        response = requests.get(api_url, params=params, timeout=150)

        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error {response.status_code}: {response.text}"

    except Exception as e:
        return None, str(e)


# -----------------------------
# MAIN LOGIC
# -----------------------------
if fetch_button:
    st.info("Connecting to Data.gov.in API...")
    
    data, error = fetch_data(api_url, api_key, limit)

    if error:
        st.error(error)
    else:
        st.success("✅ API Key is valid and data retrieved successfully!")

        # Raw JSON
        with st.expander("📦 View Raw JSON"):
            st.json(data)

        # DataFrame view
        if "records" in data and len(data["records"]) > 0:
            df = pd.DataFrame(data["records"])

            st.subheader("📊 Data Preview")
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Summary")
            col1, col2 = st.columns(2)
            col1.metric("Records Fetched", len(df))
            col2.metric("Total Columns", len(df.columns))

            # Numeric visualization
            numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

            if numeric_cols:
                selected_col = st.selectbox("Select Numeric Column to Visualize", numeric_cols)
                st.bar_chart(df[selected_col])
            else:
                st.warning("No numeric columns available for charting.")
        else:
            st.warning("No records found in API response.")