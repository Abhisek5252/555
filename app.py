import os
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import json

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "games_secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# Store active game sessions
active_games = {}

with app.app_context():
    import models
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wallet')
def wallet():
    user = models.User.query.first()
    if not user:
        user = models.User(address='demo_address')
        db.session.add(user)
        db.session.commit()
    return render_template('wallet.html', user=user)

@app.route('/games')
def games():
    user = models.User.query.first()
    if not user:
        user = models.User(address='demo_address')
        db.session.add(user)
        db.session.commit()
    return render_template('games.html', user=user)

@app.route('/api/daily-login', methods=['POST'])
def daily_login():
    user = models.User.query.first()
    if not user:
        user = models.User(address='demo_address')
        db.session.add(user)

    now = datetime.utcnow()
    if user.last_login and (now - user.last_login) < timedelta(days=1):
        return jsonify({'error': 'Already claimed today'}), 400

    reward = 150 * (2 ** user.login_streak)
    user.metarush_balance += reward
    user.last_login = now
    user.login_streak = (user.login_streak + 1) % 7
    db.session.commit()

    return jsonify({
        'reward': reward,
        'streak': user.login_streak,
        'balance': user.metarush_balance
    })

@app.route('/api/spin', methods=['POST'])
def spin_wheel():
    import random
    user = models.User.query.first()
    if random.random() < 0.01:
        prize = random.randint(100, 300)
        token_type = 'verse'
        user.metaverse_balance += prize
    else:
        prize = random.randint(10, 50)
        token_type = 'rush'
        user.metarush_balance += prize

    spin = models.SpinHistory(
        user_id=user.id,
        prize_amount=prize,
        token_type=token_type
    )
    db.session.add(spin)
    db.session.commit()

    return jsonify({
        'prize': prize,
        'token_type': token_type,
        'metarush_balance': user.metarush_balance,
        'metaverse_balance': user.metaverse_balance
    })

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')
