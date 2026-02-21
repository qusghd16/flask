from flask import Flask, request
import time

app = Flask(__name__)

first_red_time = None

@app.route('/', methods=['GET'])
def home():
    return "Server Running"

@app.route('/webhook', methods=['POST'])
def webhook():
    global first_red_time
    
    data = request.json
    signal = data.get("signal")

    now = time.time()

    if signal == "GREEN":
        first_red_time = None
        return "Reset"

    if signal == "RED":
        if first_red_time is None:
            first_red_time = now
            return "First Red Saved"
        else:
            if now - first_red_time <= 610:
                first_red_time = None
                print("SECOND RED CONFIRMED")
                return "ALERT"
            else:
                first_red_time = now
                return "Too Late"

    return "OK"
