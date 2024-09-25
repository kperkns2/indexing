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

# Calculate birthday points
def calculate_birthday_points():
    if st.session_state.red_date > st.session_state.blue_date:
        return 'Red'
    elif st.session_state.blue_date > st.session_state.red_date:
        return 'Blue'
    else:
        return 'None'

birthday_owner = calculate_birthday_points()

# Layout: Sidebar for controls
with st.sidebar:
    st.header("Game Controls")
    
    st.markdown("### Enter the Most Distant Birthday")
    st.write("Teams can set their birthdays. The team with the most recent (distant) birthday earns additional points.")
    
    st.subheader("Red Team")
    # Country Selection for Red Team
    available_countries_red = countries_df['name'][~countries_df['name'].isin(st.session_state.red_countries + st.session_state.blue_countries)].tolist()
    red_country = st.selectbox("Select a country for Red Team", options=available_countries_red, key='red_select')
    if st.button("Claim for Red", key='red_button'):
        if red_country:
            st.session_state.red_countries.append(red_country)
            st.success(f"Red Team claimed {red_country}!")
    
    # Date Selection for Red Team
    red_date = st.date_input("Select Red Team Birthday", value=st.session_state.red_date, key='red_date_input')
    st.session_state.red_date = red_date
    
    st.markdown("---")
    
    st.subheader("Blue Team")
    # Country Selection for Blue Team
    available_countries_blue = countries_df['name'][~countries_df['name'].isin(st.session_state.red_countries + st.session_state.blue_countries)].tolist()
    blue_country = st.selectbox("Select a country for Blue Team", options=available_countries_blue, key='blue_select')
    if st.button("Claim for Blue", key='blue_button'):
        if blue_country:
            st.session_state.blue_countries.append(blue_country)
            st.success(f"Blue Team claimed {blue_country}!")
    
    # Date Selection for Blue Team
    blue_date = st.date_input("Select Blue Team Birthday", value=st.session_state.blue_date, key='blue_date_input')
    st.session_state.blue_date = blue_date
    
    st.markdown("---")
    
    # Display lists of countries
    st.subheader("Red Team Countries")
    if st.session_state.red_countries:
        st.write(", ".join(st.session_state.red_countries))
    else:
        st.write("No countries claimed yet.")
    
    st.subheader("Blue Team Countries")
    if st.session_state.blue_countries:
        st.write(", ".join(st.session_state.blue_countries))
    else:
        st.write("No countries claimed yet.")

# Main area for scores and map
st.title("Red Team vs Blue Team World Domination Game")

# Calculate scores
red_score, blue_score = calculate_scores()

# Display scores and birthday points
score_col1, score_col2, score_col3 = st.columns(3)

with score_col1:
    st.markdown(f"### :red[Red Team Score: {red_score}]")
with score_col2:
    st.markdown("### 🏆 Birthday Points")
    if birthday_owner == 'Red':
        st.markdown("### :red[Red Team owns the Birthday Points]")
    elif birthday_owner == 'Blue':
        st.markdown("### :blue[Blue Team owns the Birthday Points]")
    else:
        st.markdown("### Neutral")
with score_col3:
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
    projection='natural earth',
    title="World Map: Team Ownership"
)
fig.update_layout(legend_title_text='Team Ownership')

st.plotly_chart(fig, use_container_width=True)
