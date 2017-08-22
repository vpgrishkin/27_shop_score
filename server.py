import datetime
import os

from flask import Flask, render_template, jsonify, send_from_directory, request
import psycopg2


app = Flask(__name__)

DB_CONFIG = os.getenv("DB_CONFIG")
DATA_REFRESH_INTERVAL = 10 * 1000
RED_INTERVAL = 30
YELLOW_INTERVAL = 7


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
    with psycopg2.connect("host=shopscore.devman.org dbname=shop port=5432 user=score password=Rysherat2") as conn:
        with conn.cursor() as cursor:
            nearest_unconfirmed_order_date = fetch_nearest_unconfirmed_order_date(cursor)
            count_unconfirmed_orders = fetch_count_unconfirmed_orders(cursor)
            count_orders_processed_today = fetch_count_orders_processed_today(cursor)

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


def fetch_nearest_unconfirmed_order_date(cursor):
    cursor.execute("SELECT created FROM orders WHERE confirmed IS NULL ORDER BY created DESC LIMIT 1")
    nearest_unconfirmed_order_date = cursor.fetchall()
    if nearest_unconfirmed_order_date:
        return nearest_unconfirmed_order_date[0][0]
    return 0

def fetch_count_unconfirmed_orders(cursor):
    cursor.execute("SELECT COUNT(*) FROM orders WHERE confirmed IS NULL")
    count_unconfirmed_orders = cursor.fetchall()
    if count_unconfirmed_orders:
        return count_unconfirmed_orders[0][0]
    return 0


def fetch_count_orders_processed_today(cursor):
    cursor.execute("SELECT COUNT(*) FROM orders WHERE confirmed IS NOT NULL AND created >= 'today'")
    count_orders_processed_today = cursor.fetchall()
    if count_orders_processed_today:
        return count_orders_processed_today[0][0]
    return 0


def fetch_KPI(conn):
    with conn.cursor() as cursor:
        nearest_unconfirmed_order_date = fetch_nearest_unconfirmed_order_date(cursor)
        count_unconfirmed_orders = fetch_count_unconfirmed_orders(cursor)
        count_orders_processed_today = fetch_count_orders_processed_today(cursor)


if __name__ == "__main__":
    app.run()

