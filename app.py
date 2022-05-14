import glob
import io
import os
import uuid
import numpy as np
from flask import Flask, jsonify, make_response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.secret_key = "changeforprod"
app.debug = False
app._static_folder = os.path.abspath("templates/static/")


@app.route("/", methods=["GET"])
def index():
    title = "Get Ticker Price Data"
    return render_template("layouts/index.html", title=title)


@app.route("/results/", methods=["GET"])
def results():
    title = "Results"
    datalist = []
    for csv in glob.iglob("images/*.csv"):
        datalist.append(get_file_content(csv))
    return render_template("layouts/results.html", title=title, datalist=datalist)


@app.route("/results/<unique_id>", methods=["GET"])
def result_for_uuid(unique_id):
    title = "Result"
    data = get_file_content(get_file_name(unique_id))
    return render_template("layouts/result.html", title=title, data=data)


@app.route("/postmethod", methods=["POST"])
def post_javascript_data():
    jsdata = request.form["canvas_data"]
    unique_id = create_csv(jsdata)
    params = {"unique_id": unique_id}
    return jsonify(params)

@app.route("/postticker", methods=["POST"])
def post_ticker_data():
    ticker = str(request.form["ticker_name"])
    params = {"stock": ticker}
    return jsonify(params)

@app.route("/price_chart/<ticker>")
def price_chart(ticker):
    return render_template("layouts/price_chart.html", title=ticker)

@app.route("/plot/<imgdata>")
def plot(imgdata):
    data = [float(i) for i in imgdata.strip("[]").split(",")]
    data = np.reshape(data, (200, 200))
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.axis("off")
    axis.imshow(data, interpolation="nearest")
    canvas = FigureCanvas(fig)
    output = io.BytesIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = "image/png"
    return response


def create_csv(text):
    unique_id = str(uuid.uuid4())
    with open(get_file_name(unique_id), "a") as file:
        file.write(text[1:-1] + "\n")
    return unique_id


def get_file_name(unique_id):
    return f"images/{unique_id}.csv"


def get_file_content(filename):
    with open(filename, "r") as file:
        return file.read()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
