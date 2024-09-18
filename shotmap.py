import streamlit as st
import pandas as pd
from mplsoccer import VerticalPitch,Pitch
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
import json

st.title('La Liga 2015/16 Shot Map')
st.subheader('Filter for any Team or Player to see all of their shots taken during the season')

df = pd.read_csv('shots_data_laliga1516.csv')
df = df[df['type'] == 'Shot'].reset_index(drop = True)
df['location'] = df['location'].apply(json.loads)

team = st.selectbox('Select a Team', df['team'].sort_values().unique(), index=None)

players = df['player'].sort_values().unique() if team is None else df[df['team'] == team]['player'].sort_values().unique()

player = st.selectbox('Select a Player', players, index=None)

if team:
    df = df[df['team'] == team]
if player:
    df = df[df['player'] == player]

pitch = VerticalPitch(pitch_type='statsbomb', half = True)
fig, ax = pitch.draw(figsize=(10,10))

for x in df.to_dict(orient= 'records'):
    pitch.scatter(
        x = float(x['location'][0]),
        y = float(x['location'][1]),
        ax = ax,
        s = 1000* x['shot_statsbomb_xg'],
        color = 'green' if x['shot_outcome'] == 'Goal' else 'white',
        edgecolors = 'black',
        alpha = 1 if x['type'] == 'goal' else .5,
        zorder = 2 if x['type'] == 'goal' else 1
    )

st.pyplot(fig)
    
    
