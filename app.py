import io
import os
import uuid

import numpy as np
from flask import Flask, jsonify, make_response, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)
app.secret_key = "s3cr3t"
app.debug = True
app._static_folder = os.path.abspath("templates/static/")


@app.route("/", methods=["GET"])
def index():
    title = "Create the input"
    return render_template("layouts/index.html", title=title)


@app.route("/results/<uuid>", methods=["GET"])
def results(uuid):
    title = "Result"
    data = get_file_content(uuid)
    return render_template("layouts/results.html", title=title, data=data)


@app.route("/postmethod", methods=["POST"])
def post_javascript_data():
    jsdata = request.form["canvas_data"]
    unique_id = create_csv(jsdata)
    params = {"uuid": unique_id}
    return jsonify(params)


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
    with open("images/" + unique_id + ".csv", "a") as file:
        file.write(text[1:-1] + "\n")
    return unique_id


def get_file_content(uuid):
    with open("images/" + uuid + ".csv", "r") as file:
        return file.read()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
