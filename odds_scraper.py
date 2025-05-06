
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_odds():
    url = "https://www.bestfightodds.com/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        odds_table = soup.find("table", {"class": "odds-table"})
        if not odds_table:
            return pd.DataFrame()

        rows = odds_table.find_all("tr", {"class": "odd"})

        fights = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                fighter = cols[0].text.strip()
                opponent = cols[1].text.strip()
                try:
                    odds_str = cols[2].text.strip().replace("+", "")
                    odds = float(odds_str) if odds_str else None
                except:
                    odds = None

                fights.append({
                    "fight": f"{fighter} vs {opponent}",
                    "odds_fighter_a": odds,
                    "odds_fighter_b": None  # Extend this if needed
                })

        return pd.DataFrame(fights)

    except Exception as e:
        return pd.DataFrame([{"fight": "Error loading odds", "odds_fighter_a": None, "odds_fighter_b": None}])
