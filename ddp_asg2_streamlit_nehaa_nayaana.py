import streamlit as st
import pandas as pd

st.title("Bus Arrival Timings from Google Sheets (CSV Export)")

# Function to load data from the Google Sheet CSV
def load_data_from_google_sheets():
    try:
        # URL of the published Google Sheet (replace with your own)
        sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR3tnFE4OOgrP20HQ2g5h8BWDNJISeQjQ5VnNjEB69-OnMoosodQwp49ErtBn_PEsFKxaOa8oCIhz_f/pub?output=csv"
        
        # Load the CSV into a DataFrame using pandas
        df = pd.read_csv(sheet_url)
        return df
    except Exception as e:
        st.error(f"Error loading data from Google Sheets: {e}")
        return pd.DataFrame()

# Function to display bus information
def display_bus_info(df):
    if df.empty:
        st.warning("No bus information available.")
        return

    # Display the dataframe (for testing)
    st.markdown(f"### Bus Information")
    st.write(df.head())  # Show the first few rows

# Load and display data
df = load_data_from_google_sheets()

# Display bus information if data is available
if not df.empty:
    display_bus_info(df)
else:
    st.warning("No data available to display.")
