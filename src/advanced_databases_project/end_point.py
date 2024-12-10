from flask import Flask, Response

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome! Metrics are at."


@app.route("/weather_metrics")
def weather_metrics():
    return Response("", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
