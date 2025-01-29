import streamlit as st
import pandas as pd
from io import BytesIO
import requests
from datetime import datetime

st.title("Bus Arrival Timings")

# Cache data loading for efficiency
@st.cache_data
def load_data_from_github():
    try:
        # URL of the raw Excel file on GitHub
        file_url = 'https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2Fnehaanayaana%2FDDP-ASG2-Streamlit-Nehaa-Nayaana%2Frefs%2Fheads%2Fmain%2Fdata%2FDDP_ASG2_Nehaa%2520Nayaana.xlsx&wdOrigin=BROWSELINK'
        
        # Send a GET request to fetch the file
        response = requests.get(file_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Read the content of the response into a BytesIO object
            file = BytesIO(response.content)
            
            # Load the Excel data into a DataFrame using openpyxl engine
            df = pd.read_excel(file, engine='openpyxl')
            return df
        else:
            st.error(f"Failed to load the file, status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data from GitHub: {e}")
        return pd.DataFrame()

# Function to get color-coded labels for seating status
def get_seating_status_color(status):
    status_colors = {
        "Seats Available": "green", 
        "Standing Available": "orange", 
        "Limited Standing": "red"
    }
    return status_colors.get(status, "grey")

# Function to get bus type icon
def get_bus_type_icon(bus_type):
    if bus_type == "Single Deck":
        return "🚌"
    elif bus_type == "Double Deck":
        return "🚍"
    return "🚌"  # Fallback icon

# Display bus information
def display_bus_info(df):
    if df.empty:
        st.warning("No bus information available.")
        return

    current_date = datetime.now().strftime("%d/%m/%Y")
    st.markdown(f"### Bus Information for Bus Stops Near Ngee Ann Polytechnic")
    st.write(f"📅 Current Date: **{current_date}**")

    # Group and display unique bus stops
    bus_stops = df[['Description', 'Bus Stop No.']].drop_duplicates()
    bus_stop_selection = st.radio("Select Bus Stop", bus_stops['Description'].tolist(), index=0)
    selected_bus_stop_code = bus_stops.loc[bus_stops['Description'] == bus_stop_selection, 'Bus Stop No.'].values[0]

    # Filter buses at the selected bus stop
    stop_buses = df[df['Bus Stop No.'] == selected_bus_stop_code]

    if stop_buses.empty:
        st.write("No bus information available for this stop.")
        return

    st.markdown(f"#### 🚏 Bus Stop Code: **{selected_bus_stop_code}**")
    st.markdown(f"**{bus_stop_selection}**")

    # Remove duplicates and sort by 'MinutesToArrival'
    stop_buses = stop_buses.drop_duplicates(subset=['ServiceNo', 'IncomingBus'])
    stop_buses = stop_buses.sort_values(by='MinutesToArrival', ascending=True)

    # Group buses by ServiceNo
    buses = stop_buses.groupby('ServiceNo')

    for bus_no, group in buses:
        # Add a border around the service number and its arrival details
        with st.container():
            # Create a bordered box for each service
            st.markdown(f"<div style='border: 2px solid #ddd; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

            # Display the service number as a heading
            st.markdown(f"### **Service No: {bus_no}**")

            # Display up to three arrival widgets for each service
            arrivals = group[['IncomingBus', 'MinutesToArrival', 'EstimatedTimeArrival', 'Load', 'Operator', 'Feature', 'Type', 'FrequencyRange']].head(3)

            if arrivals.empty:
                st.write("No upcoming arrivals for this bus.")
                continue

            # Create columns dynamically based on the number of arrivals
            num_arrivals = len(arrivals)
            cols = st.columns(num_arrivals)

            for idx, (index, row) in enumerate(arrivals.iterrows()):
                minutes_left = row['MinutesToArrival']
                estimated_time = row['EstimatedTimeArrival']
                seating_status = row['Load']
                operator = row['Operator']
                wheelchair_accessible = "♿" if row['Feature'] == "Wheelchair Accessible" else ""
                bus_type = get_bus_type_icon(row['Type'])
                color = get_seating_status_color(seating_status)

                with cols[idx]:
                    # Display the bus arrival details inside the columns
                    st.markdown(f"<div style='border: 2px solid #eee; padding: 15px; border-radius: 5px;'>", unsafe_allow_html=True)

                    # Display the bus type icon
                    bus_icon = get_bus_type_icon(row['Type'])

                    # Display minutes until arrival
                    st.markdown(f"<div style='text-align:center; font-size:30px; color:{color}; font-weight:bold;'>{minutes_left} mins</div>", unsafe_allow_html=True)

                    # Display both bus icon and wheelchair accessibility
                    if wheelchair_accessible:
                        st.markdown(f"<div style='text-align:center; font-size:30px;'>"
                                    f"{bus_icon} <span style='font-size:20px;'> ♿ </span></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='text-align:center; font-size:30px;'>{bus_icon}</div>", unsafe_allow_html=True)

                    # Display the rest of the details
                    st.markdown(f"- **Arrival Time:** {estimated_time}")

                    # Expander for viewing more details if needed
                    with st.expander(f"View More for Bus {bus_no}"):

                        st.markdown(f"- **Seating Status:** <span style='color:{color}; font-weight:bold;'>{seating_status}</span>", unsafe_allow_html=True)
                        st.markdown(f"- **Wheelchair Accessible:** {row['Feature']}")
                        st.markdown(f"- **Operator:** {row['Operator']}")
                        st.markdown(f"- **Frequency Range:** {row['FrequencyRange']}")

                    st.markdown("</div>", unsafe_allow_html=True)

            # Close the main service box
            st.markdown("</div>", unsafe_allow_html=True)

# Load data from GitHub
df = load_data_from_github()

# Display bus information
if not df.empty:
    display_bus_info(df)
else:
    st.warning("No data available to display.")
