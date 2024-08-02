import streamlit as st
import mysql.connector
import pandas as pd

# Set up the MySQL connection
db_connection = mysql.connector.connect(
    host="localhost",  
    user="root",       
    password="password",  
    database="redbus_1"  
)
cursor = db_connection.cursor(dictionary=True)

# Fetch data from the database
cursor.execute("SELECT * FROM bus_routes")
data = cursor.fetchall()

# Close the database connection
cursor.close()
db_connection.close()

# Convert data to a pandas DataFrame
df = pd.DataFrame(data)

# Extract hours, minutes, and seconds from the timedelta64[ns] format
df["departing_time"] = df["departing_time"].apply(lambda x: (pd.Timedelta(seconds=x.total_seconds())).components)
df["reaching_time"] = df["reaching_time"].apply(lambda x: (pd.Timedelta(seconds=x.total_seconds())).components)

# Format the time columns to HH:MM:SS
df["departing_time"] = df["departing_time"].apply(lambda x: f"{int(x.hours):02}:{int(x.minutes):02}:{int(x.seconds):02}")
df["reaching_time"] = df["reaching_time"].apply(lambda x: f"{int(x.hours):02}:{int(x.minutes):02}:{int(x.seconds):02}")

# Fill None values in the price column with 0 and convert to integers
df["price"] = df["price"].fillna(0).astype(int)

# Streamlit application layout
st.set_page_config(page_title="Bus Routes Dashboard", layout="wide")

# Streamlit theme settings
st.markdown(
    """
    <style>
    .main {
        background-color: #FFC0CB;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Bus Routes Dashboard")
st.markdown("## Explore and Analyze Bus Routes Information")

# Sidebar filters
st.sidebar.header("Filter Data")
route_name = st.sidebar.selectbox("Select Route Name", ["All"] + list(df["route_name"].unique()))
bus_name = st.sidebar.selectbox("Select Bus Name", ["All"] + list(df["busname"].unique()))
bus_type = st.sidebar.selectbox("Select Bus Type", ["All"] + list(df["bustype"].unique()))
min_star_rating = st.sidebar.slider("Minimum Star Rating", min_value=0.0, max_value=5.0, step=0.1, value=0.0)
max_price = st.sidebar.slider("Maximum Price", min_value=0, max_value=7619, step=10, value=7619)

# Filter the data based on selections
filtered_data = df[
    ((df["route_name"] == route_name) if route_name != "All" else True) &
    ((df["busname"] == bus_name) if bus_name != "All" else True) &
    ((df["bustype"] == bus_type) if bus_type != "All" else True) &
    (df["star_rating"] >= min_star_rating) &
    (df["price"] <= max_price)
]

# Display filtered data
st.markdown("### Filtered Data")
st.write(filtered_data)

# Detailed view for each bus
st.markdown("### Bus Details")
for i, row in filtered_data.iterrows():
    st.subheader(f"Bus {i + 1}")
    st.write(f"**Route Name**: {row['route_name']}")
    st.write(f"**Bus Name**: {row['busname']}")
    st.write(f"**Bus Type**: {row['bustype']}")
    st.write(f"**Departing Time**: {row['departing_time']}")
    st.write(f"**Duration**: {row['duration']}")
    st.write(f"**Reaching Time**: {row['reaching_time']}")
    st.write(f"**Star Rating**: {row['star_rating']}")
    st.write(f"**Price**: {row['price']}")
    st.write(f"**Seats Available**: {row['seats_available']}")

# Charts
st.markdown("### Data Visualization")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Star Rating Distribution")
    st.bar_chart(filtered_data['star_rating'].value_counts())

with col2:
    st.markdown("#### Price Distribution")
    st.bar_chart(filtered_data['price'].value_counts())

st.markdown("#### Bus Type Count")
st.bar_chart(filtered_data['bustype'].value_counts())

st.markdown("#### Route Name Count")
st.bar_chart(filtered_data['route_name'].value_counts())
