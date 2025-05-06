
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=60000, key="auto_refresh")  # Refresh every 60 seconds


import streamlit as st
import pandas as pd
import datetime
from bankroll_manager import load_bankroll, log_bet, get_bankroll_history
from odds_scraper import get_odds
import joblib
import numpy as np

# Load model
model = joblib.load("fightiq_stacked90_meta_model.pkl")

st.title("💸 FightEdge – Value Betting Tracker")

# Load bankroll
bankroll = load_bankroll()

st.sidebar.header("📊 Bankroll Info")
st.sidebar.write(f"**Current Bankroll:** £{bankroll:.2f}")

# Display bankroll chart
history = get_bankroll_history()
if not history.empty:
    st.line_chart(history.set_index("date")["bankroll"])

# Scrape odds
st.header("📡 Live Odds (Sample Data)")
odds_df = get_odds()
st.dataframe(odds_df)

# Select fight
fight = st.selectbox("Select a fight", odds_df["fight"])
selected = odds_df[odds_df["fight"] == fight].iloc[0]

# Input model probabilities
st.subheader("🤖 Model Win Probability (Enter manually)")
model_prob = st.slider("Model win % for Fighter A", 0.0, 1.0, 0.55, 0.01)
bookie_prob = 1 / selected["odds_fighter_a"]

# Calculate edge
edge = model_prob - bookie_prob
kelly_fraction = max(0.0, edge / (1 - bookie_prob))
recommended_bet = kelly_fraction * bankroll

st.markdown(f"**Edge:** {edge:.2%}")
st.markdown(f"**Recommended Bet:** £{recommended_bet:.2f} ({kelly_fraction:.2%} of bankroll)")

# Manual bet logging
if st.button("💰 Place Bet"):
    log_bet(fight=selected["fight"], 
            fighter="Fighter A", 
            model_prob=model_prob, 
            bookie_odds=selected["odds_fighter_a"],
            bet_amount=recommended_bet,
            result=None)
    st.success("Bet logged. Update result later.")


# -------------------------------------
# New Tabs for Result Tracking and Stats
# -------------------------------------
st.header("📈 Bet Result Tracker")
df = get_bankroll_history()
if not df.empty:
    for i in range(len(df)):
        row = df.iloc[i]
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.write(f"{row['date']} – {row['fight']} – £{row['bet_amount']:.2f}")
        with col2:
            if row['result'] is None or pd.isna(row['result']):
                if st.button(f"✅ Win", key=f"win_{i}"):
                    update_result(i, "win")
                    st.experimental_rerun()
        with col3:
            if row['result'] is None or pd.isna(row['result']):
                if st.button(f"❌ Loss", key=f"loss_{i}"):
                    update_result(i, "loss")
                    st.experimental_rerun()

st.header("📊 Betting Analytics")
stats = get_stats()
st.markdown(f"**Total Bets:** {stats['total_bets']}")
st.markdown(f"**Wins:** {stats['wins']}")
st.markdown(f"**Losses:** {stats['losses']}")
st.markdown(f"**ROI:** {stats['roi']:.2%}")
st.markdown(f"**Avg Edge:** {stats['avg_edge']:.2%}")
