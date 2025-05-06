
import pandas as pd
import os
from datetime import datetime

BANKROLL_FILE = "data/bankroll.csv"

def load_bankroll():
    if not os.path.exists(BANKROLL_FILE):
        pd.DataFrame([{"date": datetime.today().date(), "bankroll": 100.0}]).to_csv(BANKROLL_FILE, index=False)
    df = pd.read_csv(BANKROLL_FILE)
    return df.iloc[-1]["bankroll"]

def get_bankroll_history():
    if not os.path.exists(BANKROLL_FILE):
        return pd.DataFrame()
    return pd.read_csv(BANKROLL_FILE)

def log_bet(fight, fighter, model_prob, bookie_odds, bet_amount, result=None):
    history = get_bankroll_history()
    bankroll = history.iloc[-1]["bankroll"] if not history.empty else 100.0
    new_entry = {
        "date": datetime.today().date(),
        "fight": fight,
        "fighter": fighter,
        "model_prob": model_prob,
        "bookie_odds": bookie_odds,
        "bet_amount": bet_amount,
        "result": result,
        "profit": None,
        "bankroll": bankroll - bet_amount
    }
    history = pd.concat([history, pd.DataFrame([new_entry])], ignore_index=True)
    history.to_csv(BANKROLL_FILE, index=False)

def update_result(index, result):
    df = get_bankroll_history()
    if index >= len(df):
        return
    if result == "win":
        profit = df.loc[index, "bet_amount"] * (df.loc[index, "bookie_odds"] - 1)
        df.loc[index, "result"] = "win"
        df.loc[index, "profit"] = profit
    elif result == "loss":
        df.loc[index, "result"] = "loss"
        df.loc[index, "profit"] = -df.loc[index, "bet_amount"]
    # Recalculate bankroll forward
    bankroll = 100.0
    for i in range(len(df)):
        bankroll -= df.loc[i, "bet_amount"]
        if pd.notnull(df.loc[i, "profit"]):
            bankroll += df.loc[i, "profit"]
        df.loc[i, "bankroll"] = bankroll
    df.to_csv(BANKROLL_FILE, index=False)

def get_stats():
    df = get_bankroll_history()
    if df.empty:
        return {"total_bets": 0, "wins": 0, "losses": 0, "roi": 0.0, "avg_edge": 0.0}
    df = df.dropna(subset=["result", "profit"])
    total_bets = len(df)
    wins = (df["result"] == "win").sum()
    losses = (df["result"] == "loss").sum()
    roi = df["profit"].sum() / df["bet_amount"].sum() if df["bet_amount"].sum() > 0 else 0.0
    avg_edge = (df["model_prob"] - 1 / df["bookie_odds"]).mean()
    return {
        "total_bets": total_bets,
        "wins": wins,
        "losses": losses,
        "roi": roi,
        "avg_edge": avg_edge
    }
