import streamlit as st
import pickle
import pandas as pd

# Load the model
pipe = pickle.load(open('ipl.pkl', 'rb'))

# Page config
st.set_page_config(page_title="IPL Win Predictor", layout="centered", page_icon="🏏")

# Custom CSS for styling
st.markdown("""
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
        color: #222;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding: 1rem 0;
    }

    /* Main container card */
    .main {
        max-width: 720px;
        margin: 0 auto;
        background: white;
        padding: 2rem 3rem;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }

    /* Title */
    h1 {
        text-align: center;
        color: #004d40;
        font-weight: 900;
        margin-bottom: 1.5rem;
        font-size: 3rem;
    }

    /* Input labels styling */
    label, .stSelectbox label, .stNumberInput label {
        font-weight: 700;
        color: #004d40;
        font-size: 1.1rem;
    }

    /* Predict Button */
    .stButton>button {
        background-color: #00796b;
        color: white;
        font-weight: 700;
        padding: 0.6rem 1.8rem;
        border-radius: 10px;
        transition: background-color 0.3s ease;
        font-size: 1.1rem;
        margin-top: 1rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #004d40;
        cursor: pointer;
        transform: scale(1.05);
    }

    /* Probability result container */
    .probability-box {
        background-color: #e0f2f1;
        border-radius: 15px;
        padding: 1.5rem 2rem;
        margin-top: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }

    /* Probability bars wrapper */
    .bar-container {
        width: 100%;
        background-color: #b2dfdb;
        border-radius: 12px;
        height: 26px;
        margin-top: 0.3rem;
        overflow: hidden;
    }

    /* Win bar style */
    .win-bar {
        height: 26px;
        background: linear-gradient(90deg, #00bfa5, #1de9b6);
        border-radius: 12px 0 0 12px;
        transition: width 1.5s ease-in-out;
    }

    /* Loss bar style */
    .loss-bar {
        height: 26px;
        background: linear-gradient(90deg, #e53935, #ef5350);
        border-radius: 12px 0 0 12px;
        transition: width 1.5s ease-in-out;
    }

    /* Headings for probabilities */
    .prob-heading {
        font-weight: 800;
        margin-bottom: 0.15rem;
    }

    /* Winning Probability Box */
    .win-prob-box {
        background-color: #e3f2fd;  /* light blue */
        border: 2px solid #1976d2;  /* blue border */
        border-radius: 20px;
        padding: 20px 30px;
        margin-top: 30px;
        box-shadow: 0 8px 24px rgba(25, 118, 210, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Main container div start
st.markdown('<div class="main">', unsafe_allow_html=True)

# Title
st.markdown("<h1>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)

# Teams and Cities
teams = ['Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
         'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
          'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
          'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
          'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
          'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
          'Sharjah', 'Mohali', 'Bengaluru']

# Inputs with columns
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('🏏 Select Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('🎯 Select Bowling Team', sorted(teams))

selected_city = st.selectbox('📍 Select Host City', sorted(cities))

target = st.number_input('🎯 Enter Target Score', min_value=1)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Current Score', min_value=0)
with col4:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, step=0.1)
with col5:
    wickets = st.number_input('Wickets Fallen', min_value=0, max_value=10)

# Prediction
if st.button('Predict Probability'):
    if overs == 0 or overs > 20 or target == 0:
        st.warning("Please enter valid values for overs and target.")
    else:
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_remaining = 10 - wickets
        crr = score / overs if overs > 0 else 0
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_remaining],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

        # Display results inside a dedicated winning probability box
        st.markdown('<div class="win-prob-box">', unsafe_allow_html=True)

        st.markdown(f'<div class="prob-heading">✅ {batting_team} Win Probability: <strong>{round(win*100)}%</strong></div>', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="bar-container">
                <div class="win-bar" style="width:{win*100}%"></div>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown(f'<div class="prob-heading" style="margin-top:1.5rem;">❌ {bowling_team} Win Probability: <strong>{round(loss*100)}%</strong></div>', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="bar-container">
                <div class="loss-bar" style="width:{loss*100}%"></div>
            </div>
        ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# End main container
st.markdown('</div>', unsafe_allow_html=True)
