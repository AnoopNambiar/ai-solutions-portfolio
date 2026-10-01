from flask import Flask, render_template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

NASA_API_URL = "https://science.nasa.gov/wp-json/wp/v2/apod-basic"
NASA_API_KEY = os.getenv("NASA_API_KEY")


@app.route("/")
def home():

    params = {
        "api_key": NASA_API_KEY
    }

    response = requests.get(
        NASA_API_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    apod = response.json()


    return render_template("index.html", apod=apod[0])

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )