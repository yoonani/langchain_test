import streamlit as st
import pandas as pd 
import numpy as np 

st.title("yoonani's streamlit test")

# Fetch data
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# caching
@st.cache_data
def load_data(nrows=None):
    if nrows:
        data = pd.read_csv(DATA_URL, nrows=nrows)
    else:
        data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# text replacement
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')

# Load 10,000 rows of data into the dataframe.
data = load_data()

# Notify the reader that the data was successfully loaded.
data_load_state.text('Done! (using st.cache_data)')


# Inspect the raw data
# toggle
if st.checkbox("Show raw data") :
    st.subheader("Raw data")
    st.write( data )    # st.dataframe 존재

# Draw a historgram
st.subheader("Number of pickups by hours")
# numpy : histogram object
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins = 24, range=(0,24))[0]
st.bar_chart( hist_values )

# Plot data on a map
hour_to_filter = 17

# filter results with a slider
hour_to_filter = st.slider('hour', 0, 23, 17)

filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter ]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map( filtered_data )          # st.pydeck_chart : complex map data