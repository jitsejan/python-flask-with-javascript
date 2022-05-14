import glob
import io
import os
import uuid
import numpy as np
from flask import Flask, jsonify, make_response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import yfinance as yf
import pendulum
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = "changeforprod"
app.debug = False
app._static_folder = os.path.abspath("templates/static/")


@app.route("/", methods=["GET"])
def index():
    title = "Get Ticker Price Data"
    return render_template("layouts/index.html", title=title)

@app.route("/postmethod", methods=["POST"])
def post_ticker_data():
    ticker = str(request.form["ticker_name"])
    params = {"stock": ticker}
    return jsonify(params)

@app.route("/price_chart/<ticker>")
def price_chart(ticker):
    return render_template("layouts/price_chart.html", title=ticker, ticker=ticker)

@app.route("/plot/<pricedata>")
def plot(pricedata):
    price_history = yf.Ticker('AAPL').history(period='5y', interval='1wk', actions=False)
    return pricedata
    #time_series = list(price_history['Open'])
    #dt_list = [pendulum.parse(str(dt)).float_timestamp for dt in list(price_history.index)]
    #plt.style.use('dark_background')
    #plt.plot(dt_list, time_series, linewidth=2)
    # output = io.BytesIO()
    #     canvas.print_png(output)
    #     response = make_response(output.getvalue())
    #     response.mimetype = "image/png"
    #     return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
