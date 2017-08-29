import datetime
import os

from flask import Flask, render_template, jsonify, send_from_directory, request
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Date, cast


DB_CONFIG = os.getenv("DB_CONFIG")
DATA_REFRESH_INTERVAL = 10 * 1000
RED_INTERVAL = 30
YELLOW_INTERVAL = 7

app = Flask(__name__)
base = automap_base()
engine = create_engine(DB_CONFIG)
base.prepare(engine, reflect=True)
orders = base.classes.orders
session = Session(engine)


@app.route('/')
def score():
    return render_template('score.html', DATA_REFRESH_INTERVAL=DATA_REFRESH_INTERVAL, RED_INTERVAL=RED_INTERVAL, YELLOW_INTERVAL=YELLOW_INTERVAL)


@app.route('/robots.txt')
def fetch_robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/style.css')
def fetch_style_css():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/kpi.json')
def fetch_kpi_json():
    nearest_unconfirmed_order_date = fetch_nearest_unconfirmed_order_date()
    count_unconfirmed_orders = fetch_count_unconfirmed_orders()
    count_orders_processed_today = fetch_count_orders_processed_today()

    order_waiting_time = get_delta_from_now_in_sec(nearest_unconfirmed_order_date)

    return jsonify({'order_waiting_time': order_waiting_time,
                    'count_unconfirmed_orders': count_unconfirmed_orders,
                    'count_orders_processed_today': count_orders_processed_today
                    })


def get_delta_from_now_in_sec(date):
        if date:
            time_delta = datetime.datetime.now() - date
            return time_delta.seconds
        return 0


def fetch_nearest_unconfirmed_order_date():
    nearest_unconfirmed_order = session.query(orders).filter(orders.confirmed.is_(None)).order_by(orders.created).first()
    if nearest_unconfirmed_order:
        return nearest_unconfirmed_order.created
    return 0


def fetch_count_unconfirmed_orders():
    count_unconfirmed_orders = session.query(orders).filter(orders.confirmed.is_(None)).count()
    if count_unconfirmed_orders:
        return count_unconfirmed_orders
    return 0


def fetch_count_orders_processed_today():
    count_orders_processed_today = session.query(orders).filter(cast(orders.confirmed, Date) == datetime.date.today()).count()
    if count_orders_processed_today:
        return count_orders_processed_today
    return 0


def fetch_KPI(conn):
        nearest_unconfirmed_order_date = fetch_nearest_unconfirmed_order_date()
        count_unconfirmed_orders = fetch_count_unconfirmed_orders()
        count_orders_processed_today = fetch_count_orders_processed_today()


if __name__ == "__main__":
    app.run()

