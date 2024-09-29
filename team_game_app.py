import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ==============================
# Initialize Session State
# ==============================

if 'red_states' not in st.session_state:
    st.session_state.red_states = []
if 'blue_states' not in st.session_state:
    st.session_state.blue_states = []
if 'red_date' not in st.session_state:
    st.session_state.red_date = datetime.today()
if 'blue_date' not in st.session_state:
    st.session_state.blue_date = datetime.today()
if 'red_select' not in st.session_state:
    st.session_state.red_select = "Select a state"
if 'blue_select' not in st.session_state:
    st.session_state.blue_select = "Select a state"

# ==============================
# Load US States Data
# ==============================

@st.cache_data
def load_states():
    us_states = [
        {'name': 'Alabama', 'abbr': 'AL'},
        {'name': 'Alaska', 'abbr': 'AK'},
        {'name': 'Arizona', 'abbr': 'AZ'},
        {'name': 'Arkansas', 'abbr': 'AR'},
        {'name': 'California', 'abbr': 'CA'},
        {'name': 'Colorado', 'abbr': 'CO'},
        {'name': 'Connecticut', 'abbr': 'CT'},
        {'name': 'Delaware', 'abbr': 'DE'},
        {'name': 'Florida', 'abbr': 'FL'},
        {'name': 'Georgia', 'abbr': 'GA'},
        {'name': 'Hawaii', 'abbr': 'HI'},
        {'name': 'Idaho', 'abbr': 'ID'},
        {'name': 'Illinois', 'abbr': 'IL'},
        {'name': 'Indiana', 'abbr': 'IN'},
        {'name': 'Iowa', 'abbr': 'IA'},
        {'name': 'Kansas', 'abbr': 'KS'},
        {'name': 'Kentucky', 'abbr': 'KY'},
        {'name': 'Louisiana', 'abbr': 'LA'},
        {'name': 'Maine', 'abbr': 'ME'},
        {'name': 'Maryland', 'abbr': 'MD'},
        {'name': 'Massachusetts', 'abbr': 'MA'},
        {'name': 'Michigan', 'abbr': 'MI'},
        {'name': 'Minnesota', 'abbr': 'MN'},
        {'name': 'Mississippi', 'abbr': 'MS'},
        {'name': 'Missouri', 'abbr': 'MO'},
        {'name': 'Montana', 'abbr': 'MT'},
        {'name': 'Nebraska', 'abbr': 'NE'},
        {'name': 'Nevada', 'abbr': 'NV'},
        {'name': 'New Hampshire', 'abbr': 'NH'},
        {'name': 'New Jersey', 'abbr': 'NJ'},
        {'name': 'New Mexico', 'abbr': 'NM'},
        {'name': 'New York', 'abbr': 'NY'},
        {'name': 'North Carolina', 'abbr': 'NC'},
        {'name': 'North Dakota', 'abbr': 'ND'},
        {'name': 'Ohio', 'abbr': 'OH'},
        {'name': 'Oklahoma', 'abbr': 'OK'},
        {'name': 'Oregon', 'abbr': 'OR'},
        {'name': 'Pennsylvania', 'abbr': 'PA'},
        {'name': 'Rhode Island', 'abbr': 'RI'},
        {'name': 'South Carolina', 'abbr': 'SC'},
        {'name': 'South Dakota', 'abbr': 'SD'},
        {'name': 'Tennessee', 'abbr': 'TN'},
        {'name': 'Texas', 'abbr': 'TX'},
        {'name': 'Utah', 'abbr': 'UT'},
        {'name': 'Vermont', 'abbr': 'VT'},
        {'name': 'Virginia', 'abbr': 'VA'},
        {'name': 'Washington', 'abbr': 'WA'},
        {'name': 'West Virginia', 'abbr': 'WV'},
        {'name': 'Wisconsin', 'abbr': 'WI'},
        {'name': 'Wyoming', 'abbr': 'WY'},
        {'name': 'District of Columbia', 'abbr': 'DC'}
    ]
    df = pd.DataFrame(us_states)
    return df

states_df = load_states()

# ==============================
# Helper Functions
# ==============================

def get_state_color(row):
    if row['name'] in st.session_state.red_states:
        return 'Red'
    elif row['name'] in st.session_state.blue_states:
        return 'Blue'
    else:
        return 'Unclaimed'

def calculate_scores():
    red_score = len(st.session_state.red_states)
    blue_score = len(st.session_state.blue_states)
    
    # Compare dates for bonus points (earliest date gets bonus)
    if st.session_state.red_date < st.session_state.blue_date:
        red_score += 10
    elif st.session_state.blue_date < st.session_state.red_date:
        blue_score += 10
    
    return red_score, blue_score

def calculate_birthday_points():
    """
    Determine which team owns the date points based on the earliest date.
    Returns 'Red', 'Blue', or 'None'.
    """
    if st.session_state.red_date < st.session_state.blue_date:
        return 'Red'
    elif st.session_state.blue_date < st.session_state.red_date:
        return 'Blue'
    else:
        return 'None'

# ==============================
# Callback Functions
# ==============================

def claim_red():
    selected = st.session_state.red_select
    if selected != "Select a state":
        if selected not in st.session_state.red_states and selected not in st.session_state.blue_states:
            st.session_state.red_states.append(selected)
            st.session_state.red_select = "Select a state"
            st.success(f"**Red Team** claimed **{selected}**!")
        else:
            st.warning("This state has already been claimed.")
    else:
        st.warning("Please select a valid state to claim.")

def claim_blue():
    selected = st.session_state.blue_select
    if selected != "Select a state":
        if selected not in st.session_state.red_states and selected not in st.session_state.blue_states:
            st.session_state.blue_states.append(selected)
            st.session_state.blue_select = "Select a state"
            st.success(f"**Blue Team** claimed **{selected}**!")
        else:
            st.warning("This state has already been claimed.")
    else:
        st.warning("Please select a valid state to claim.")

# ==============================
# Layout: Sidebar for Controls
# ==============================

with st.sidebar:
    st.header("🎮 Game Controls")
    
    st.markdown("### 📅 Enter a Date")
    st.write("Teams can set any date. The team with the earliest date earns additional points.")
    
    st.subheader("Red Team")
    available_states_red = ["Select a state"] + states_df['name'][~states_df['name'].isin(st.session_state.red_states + st.session_state.blue_states)].tolist()
    st.selectbox("Select a state for Red Team", options=available_states_red, key='red_select')
    st.button("Claim for Red", on_click=claim_red, key='red_button')
    
    # Date Selection for Red Team
    st.session_state.red_date = st.date_input(
        "Select Red Team Date",
        value=st.session_state.red_date,
        key='red_date_input'
    )
    
    st.markdown("---")
    
    st.subheader("Blue Team")
    available_states_blue = ["Select a state"] + states_df['name'][~states_df['name'].isin(st.session_state.red_states + st.session_state.blue_states)].tolist()
    st.selectbox("Select a state for Blue Team", options=available_states_blue, key='blue_select')
    st.button("Claim for Blue", on_click=claim_blue, key='blue_button')
    
    # Date Selection for Blue Team
    st.session_state.blue_date = st.date_input(
        "Select Blue Team Date",
        value=st.session_state.blue_date,
        key='blue_date_input'
    )
    
    st.markdown("---")
    
    st.subheader("Red Team States")
    if st.session_state.red_states:
        st.write(", ".join(st.session_state.red_states))
    else:
        st.write("No states claimed yet.")
    
    st.subheader("Blue Team States")
    if st.session_state.blue_states:
        st.write(", ".join(st.session_state.blue_states))
    else:
        st.write("No states claimed yet.")

# ==============================
# Main Area: Scores and Map
# ==============================

st.title("🌍 Red Team vs Blue Team US Domination Game")

# Calculate scores
red_score, blue_score = calculate_scores()

# Display scores and date points
score_col1, score_col2, score_col3 = st.columns(3)

with score_col1:
    st.markdown(
        f"### <span style='color:red'>Red Team Score: {red_score}</span>",
        unsafe_allow_html=True
    )
with score_col2:
    st.markdown("### 🗓️ Date Points")
    
    # Recalculate date points dynamically to ensure it's responsive to date changes
    birthday_owner = calculate_birthday_points()
    
    if birthday_owner == 'Red':
        st.markdown(
            "### <span style='color:red'>Red Team owns the Date Points!</span>",
            unsafe_allow_html=True
        )
    elif birthday_owner == 'Blue':
        st.markdown(
            "### <span style='color:blue'>Blue Team owns the Date Points!</span>",
            unsafe_allow_html=True
        )
    else:
        st.markdown("### ⚖️ **Neutral**")
with score_col3:
    st.markdown(
        f"### <span style='color:blue'>Blue Team Score: {blue_score}</span>",
        unsafe_allow_html=True
    )

st.markdown("---")

# Display the map
map_df = states_df.copy()
map_df['color'] = map_df.apply(get_state_color, axis=1)

fig = px.choropleth(
    map_df,
    locations='abbr',
    locationmode='USA-states',
    color='color',
    hover_name='name',
    color_discrete_map={
        'Red': 'red',
        'Blue': 'blue',
        'Unclaimed': 'lightgray'
    },
    scope='usa',
    title="🌍 US Map: Team Ownership"
)
fig.update_layout(legend_title_text='Team Ownership')

st.plotly_chart(fig, use_container_width=True)
