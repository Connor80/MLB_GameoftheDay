from flask import Flask, request as REQUEST, redirect
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)
app.config.from_object('config')

@app.route("/", methods=['GET', 'POST'])
def index():
    schedule = BackgroundScheduler(daemon=True)
    schedule.add_job(daily_update, 'cron', hour='*/12')
    schedule.start()

    text = "Checking for free game..."

    return text

def daily_update():
    account_sid = app.config['ACCOUNTSID']
    auth_token  = app.config['AUTHTOKEN']
    client = Client(account_sid, auth_token)

    url = 'https://www.mlb.com/live-stream-games'
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, 'html.parser')

    for game in soup.findAll("tr", {"class":"free-game"}):
        result = game.get_text()
    matchup = " ".join(result.split())

    if "Braves" in matchup:
        message = client.messages \
                        .create(
                             body=" ".join(result.split()),
                             from_=app.config['FROM'],
                             to=app.config['TO']
                         )


if __name__ == "__main__":
    app.run(debug=True)
