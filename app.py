import streamlit as st
import datetime
import requests
import pandas as pd
import numpy as np

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''


#date and time

pickup_datetime = st.datetime_input(
    "Select a date and time",
    datetime.datetime(2014, 7, 6, 19, 18),
)
st.write("Date and time set for", pickup_datetime)

pickup_longitude = st.number_input('Input a pickup longitude')
st.write('The pickup longitude is ', pickup_longitude)
pickup_latitude = st.number_input('Input a pickup latitude')
st.write('The pickup latitude is ', pickup_latitude)

dropoff_longitude = st.number_input('Input a dropoff longitude')
st.write('The dropoff longitude is ', dropoff_longitude)
dropoff_latitude = st.number_input('Input a dropoff latitude')
st.write('The dropoff latitude is ', dropoff_latitude)

passenger_count = st.slider('Select a line count', 1, 10, 3)
st.write('The passenger count is ', passenger_count)


def get_map_data():

    return pd.DataFrame(
    {
        "col1": np.array([pickup_latitude, dropoff_latitude]),
        "col2": np.array([pickup_longitude, dropoff_longitude]),
        "color": ["#0044ff", "#ff0000"],
    }
)

df = get_map_data()

st.map(data=df, latitude="col1", longitude="col2", color="color")

'''
## Once we have these, let's call our API in order to retrieve a prediction

See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

🤔 How could we call our API ? Off course... The `requests` package 💡
'''

url = 'https://taxifare.lewagon.ai/predict'

#2. Let's build a dictionary containing the parameters for our API...

data = dict(
          pickup_datetime= pickup_datetime,
          pickup_longitude=pickup_longitude,
          pickup_latitude=pickup_latitude,
          dropoff_longitude=dropoff_longitude,
          dropoff_latitude=dropoff_latitude,
          passenger_count=int(passenger_count),
)

#3. Let's call our API using the `requests` package...

if st.button("Predict"):
  response = requests.get(url=url, params=data)
  try:
    response.raise_for_status()
    prediction = response.json()['fare']
    st.success(f'The fare amount is equal to {prediction}', icon="🚀")
  except requests.exceptions.HTTPError as e:
    st.error(f'The API rejected the call: {e}')

