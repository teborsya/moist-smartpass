import threading
import asyncio
import aiohttp
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# --------------------------
# Flask + SocketIO Setup
# --------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')  # threading works with console input

# Store scanned student data
scanned_students = []

@app.route("/")
def index():
    return render_template("index_dark.html", scanned_students=scanned_students)

def push_student_to_clients(student_data):
    scanned_students.append(student_data)
    socketio.emit('new_student', student_data)

# --------------------------
# Async QR Scanner Logic
# --------------------------
API_BASE = "https://smartpass.moist.edu.ph/api/external"
API_TOKEN = "moist_kuV+oWpXLp7QfMXN6IzrPebwqAd2xzqc"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

async def check_student(session, student_id):
    url = f"{API_BASE}/students/{student_id}"
    try:
        async with session.get(url, headers=HEADERS, timeout=5) as response:
            response.raise_for_status()
            data = await response.json()
            return data  # return full student info
    except Exception as e:
        print("⚠️ Failed to check student:", e)
        return None

async def submit_log(session, student_id, log_type="IN"):
    url = f"{API_BASE}/student-logs"
    payload = {"student_id": int(student_id), "log_type": log_type}
    try:
        async with session.post(url, headers=HEADERS, json=payload, timeout=5) as response:
            response.raise_for_status()
            return True
    except Exception as e:
        print("⚠️ Failed to submit log:", e)
        return False

async def qr_loop():
    async with aiohttp.ClientSession() as session:
        while True:
            student_id = input("Enter QR / Student ID: ").strip()
            if not student_id.isdigit():
                print("❌ Invalid student ID")
                continue

            student_data = await check_student(session, student_id)
            if student_data:
                success = await submit_log(session, student_id, "IN")
                if success:
                    print(f"✅ Log submitted successfully: {student_data}")
                    push_student_to_clients(student_data)
            else:
                print(f"❌ Student {student_id} does not exist")

            await asyncio.sleep(0.5)

# --------------------------
# Run Flask in thread & QR scanner in async loop
# --------------------------
def run_flask():
    socketio.run(app, host='0.0.0.0', port=5001)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print("🌐 Flask running at http://localhost:5001")
    print("⌨️ QR Scanner simulation (type student ID)")

    try:
        asyncio.run(qr_loop())
    except KeyboardInterrupt:
        print("\n🛑 Program terminated")
