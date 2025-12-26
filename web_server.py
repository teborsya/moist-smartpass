# web_server.py

import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

scanned_qrs = []


@app.route("/")
def index():
    return "QR Scanner Web Server is running"


@app.route("/api/qrs")
def get_qrs():
    return jsonify(scanned_qrs)

@app.route("/api/push")
def push_qr(qr_value):
    scanned_qrs.append(qr_value)
    socketio.emit("qr_scanned", {"qr": qr_value})


def start_web_server():
    socketio.run(app, host="0.0.0.0", port=5001)
