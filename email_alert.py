
import smtplib
from email.mime.text import MIMEText
from bankroll_manager import get_bankroll_history, get_stats
from odds_scraper import get_odds

def send_email_alert(to_email, model):
    df = get_bankroll_history()
    stats = get_stats()
    odds = get_odds()

    # Dummy model usage placeholder
    fights = []
    for _, row in odds.iterrows():
        bookie_prob = 1 / row["odds_fighter_a"]
        model_prob = 0.60  # Replace with real model prediction
        edge = model_prob - bookie_prob
        if edge > 0:
            fights.append(f"{row['fight']}: Model {model_prob:.2%}, Bookie {bookie_prob:.2%}, Edge {edge:.2%}")

    content = f"""📊 FightEdge Daily Report

Bankroll: £{df.iloc[-1]['bankroll']:.2f}
ROI: {stats['roi']:.2%}
Win Rate: {stats['wins']}/{stats['total_bets']} ({(stats['wins'] / stats['total_bets']) if stats['total_bets'] else 0:.2%})

💰 Value Bets:
""" + "\n".join(fights)

    msg = MIMEText(content)
    msg["Subject"] = "FightEdge Daily Value Bets"
    msg["From"] = "fightedge@example.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("YOUR_EMAIL@gmail.com", "YOUR_APP_PASSWORD")
        server.send_message(msg)
