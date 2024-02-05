import streamlit as st 
import pandas as pd
import pydeck as pdk
import os

os.chdir( os.path.dirname(os.path.abspath(__file__)) )
# pandas data frame으로 json 읽기
myData = pd.read_json('./data/sgg_popMove.json') 

# GREEN_RGB = [0, 255, 0, 40]
# RED_RGB = [240, 100, 0, 40]
myalpha = ( myData['n'] / myData['n'].max() ).to_list()

output = pdk.Layer(
                "ArcLayer",
                data=myData,
                get_source_position=["long_origin", "lat_origin"],
                get_target_position=["long_dest", "lat_dest"],
                get_source_color=[240, 100, 0, myalpha],
                get_target_color=[0, 255, 0, myalpha],
                auto_highlight=True,
                width_scale=0.0001,
                get_width="n",
                width_min_pixels=3,
                width_max_pixels=30,
            )

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": 36.8323,
            "longitude": 127.8043,
            "zoom": 9,
            "pitch": 50,
        },
        layers=output,
    )
)