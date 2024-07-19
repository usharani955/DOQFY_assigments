from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone
import redis
import json
from scraper import scrape_nifty_50

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)

scheduler = BackgroundScheduler(timezone=timezone('UTC'))
scheduler.add_job(func=scrape_nifty_50, trigger="interval", minutes=5)
scheduler.start()


@app.route('/')
def home():
    data = json.loads(r.get('nifty_50_data') or '[]')
    return render_template('home.html', data=data)

if __name__ == '__main__':
    scrape_nifty_50()  
    app.run(debug=True)
