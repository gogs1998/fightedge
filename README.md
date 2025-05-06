# FightEdge

FightEdge is a value-betting web app that compares model predictions with bookmaker odds, calculates optimal bet size using the Kelly Criterion, and tracks ROI and bankroll performance over time.

## 📦 Features
- Real-time UFC odds scraping
- FightIQ model integration
- Value bet detection
- Kelly bet sizing
- Win/loss logging and bankroll tracking
- ROI and analytics dashboard
- Strategy simulator
- Daily email alert system (SMTP-ready)
- Optional 60-second auto-refresh

## 🚀 Deployment (Streamlit Cloud)
1. Sign in at [streamlit.io/cloud](https://streamlit.io/cloud)
2. Create a new app and point it to this repo or ZIP
3. Add your email config to `.streamlit/secrets.toml`:
```toml
[email]
user = "your_email@gmail.com"
password = "your_app_password"
```
4. Upload your model to `models/meta_model.pkl`
5. Deploy and start betting smart.

## 📨 Daily Email Alerts
Run `email_alert.py` with a scheduler like:
- PythonAnywhere
- GitHub Actions (cron)
- Your own server

## 🔁 Auto-Refresh
Included via `streamlit-autorefresh` – reloads app every 60 seconds.

---

Made for profit.