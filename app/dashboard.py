from flask import Flask, render_template, send_from_directory
import pandas as pd
import os

# Resolve absolute project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")

app = Flask(__name__)


@app.route("/")
def index():
    csv_path = os.path.join(OUTPUTS_DIR, "conjunction_events.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        total_events = len(df)
        high_risk = len(df[df["risk"] == "HIGH"])
        medium_risk = len(df[df["risk"] == "MEDIUM"])
        events = df.to_dict(orient="records")
    else:
        total_events = high_risk = medium_risk = 0
        events = []

    return render_template(
        "index.html",
        total_events=total_events,
        high_risk=high_risk,
        medium_risk=medium_risk,
        events=events
    )


@app.route("/outputs/<path:filename>")
def outputs(filename):
    return send_from_directory(OUTPUTS_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
    