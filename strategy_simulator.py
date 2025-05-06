
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(initial_bankroll=100.0, edge=0.05, kelly_fraction=1.0, num_bets=1000):
    bankroll = [initial_bankroll]
    for _ in range(num_bets):
        prob = 0.5 + edge
        odds = 1 / (0.5 - edge) if (0.5 - edge) > 0 else 2.0
        bet_size = bankroll[-1] * (kelly_fraction * ((prob * (odds - 1) - (1 - prob)) / (odds - 1)))
        bet_size = max(0, min(bet_size, bankroll[-1]))

        outcome = np.random.rand() < prob
        if outcome:
            bankroll.append(bankroll[-1] + bet_size * (odds - 1))
        else:
            bankroll.append(bankroll[-1] - bet_size)

    return bankroll

def display_simulator():
    st.header("🎲 Strategy Simulator")
    bankroll = st.number_input("Initial Bankroll", 0.0, 10000.0, 100.0)
    edge = st.slider("Estimated Edge", 0.0, 0.2, 0.05)
    kelly = st.slider("Kelly Fraction", 0.0, 2.0, 1.0)
    num_bets = st.slider("Number of Bets", 100, 5000, 1000)

    results = run_simulation(bankroll, edge, kelly, num_bets)
    st.line_chart(results)
