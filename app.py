"""Flask application for a web server."""

from threading import Thread
from flask import Flask, render_template
import os

app = Flask("")

# Path to your log file
LOG_FILE_PATH = 'yatirimbot.log'

@app.route("/", methods=["GET", "POST"])
def home():
    """Render the home page."""
    # Read the log file
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, 'r') as file:
            log_contents = file.readlines()
            log_contents.reverse()
    else:
        log_contents = ["Log file not found."]

    # Join the log contents into a single string for display
    log_display = ''.join(log_contents)

    # Render the index.html template with log contents
    return render_template("index.html", log_display=log_display)

def run():
    """Run the Flask application."""
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    """Start the Flask application in a separate thread."""
    t = Thread(target=run)
    t.start()
