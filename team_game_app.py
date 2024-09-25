import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
from datetime import datetime

# Initialize session state
if 'red_countries' not in st.session_state:
    st.session_state.red_countries = []
if 'blue_countries' not in st.session_state:
    st.session_state.blue_countries = []
if 'red_date' not in st.session_state:
    st.session_state.red_date = datetime.today()
if 'blue_date' not in st.session_state:
    st.session_state.blue_date = datetime.today()

# Load country data
@st.cache_data
def load_countries():
    countries = []
    for country in pycountry.countries:
        countries.append({
            'name': country.name,
            'alpha_3': country.alpha_3
        })
    df = pd.DataFrame(countries)
    return df

countries_df = load_countries()

# Function to assign color based on ownership
def get_country_color(row):
    if row['name'] in st.session_state.red_countries:
        return 'Red'
    elif row['name'] in st.session_state.blue_countries:
        return 'Blue'
    else:
        return 'LightGray'

# Calculate scores
def calculate_scores():
    red_score = len(st.session_state.red_countries)
    blue_score = len(st.session_state.blue_countries)
    
    # Compare dates
    if st.session_state.red_date < st.session_state.blue_date:
        red_score += 10
    elif st.session_state.blue_date < st.session_state.red_date:
        blue_score += 10
    # If dates are equal, no bonus points

    return red_score, blue_score

red_score, blue_score = calculate_scores()

# Layout: Scores at the top
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### :red[Red Team Score: {red_score}]")
with col2:
    st.markdown(f"### :blue[Blue Team Score: {blue_score}]")

st.markdown("---")

# Display the map
map_df = countries_df.copy()
map_df['color'] = map_df.apply(get_country_color, axis=1)

fig = px.choropleth(
    map_df,
    locations='alpha_3',
    color='color',
    hover_name='name',
    color_discrete_map={
        'Red': 'red',
        'Blue': 'blue',
        'LightGray': 'lightgray'
    },
    projection='natural earth'
)
fig.update_layout(legend_title_text='Team Ownership')

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Country selection with autocomplete using selectbox
st.header("Claim a Country")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Red Team")
    available_countries = countries_df['name'][~countries_df['name'].isin(st.session_state.red_countries + st.session_state.blue_countries)].tolist()
    red_country = st.selectbox("Select a country", options=available_countries, key='red_select')
    if st.button("Claim for Red", key='red_button'):
        if red_country:
            st.session_state.red_countries.append(red_country)
            st.success(f"Red Team claimed {red_country}!")

    st.subheader("Red Team Date")
    red_date = st.date_input("Select Red Team Date", value=st.session_state.red_date, key='red_date_input')
    st.session_state.red_date = red_date

with col2:
    st.subheader("Blue Team")
    available_countries_blue = countries_df['name'][~countries_df['name'].isin(st.session_state.red_countries + st.session_state.blue_countries)].tolist()
    blue_country = st.selectbox("Select a country", options=available_countries_blue, key='blue_select')
    if st.button("Claim for Blue", key='blue_button'):
        if blue_country:
            st.session_state.blue_countries.append(blue_country)
            st.success(f"Blue Team claimed {blue_country}!")

    st.subheader("Blue Team Date")
    blue_date = st.date_input("Select Blue Team Date", value=st.session_state.blue_date, key='blue_date_input')
    st.session_state.blue_date = blue_date

st.markdown("---")

# Recalculate scores after potential updates
red_score, blue_score = calculate_scores()

# Update the scores display
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"### :red[Red Team Score: {red_score}]")
with col2:
    st.markdown(f"### :blue[Blue Team Score: {blue_score}]")

st.markdown("---")

# Display lists of countries
col1, col2 = st.columns(2)

with col1:
    st.subheader("Red Team Countries")
    if st.session_state.red_countries:
        st.write(", ".join(st.session_state.red_countries))
    else:
        st.write("No countries claimed yet.")

with col2:
    st.subheader("Blue Team Countries")
    if st.session_state.blue_countries:
        st.write(", ".join(st.session_state.blue_countries))
    else:
        st.write("No countries claimed yet.")
