from flask import Flask, render_template, jsonify, request, json
import requests

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/verify', methods=['POST'])
def verify():
    # reCAPTCHAP server side
    recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_secret_key = '{ Your Secret Key}'
    payload = {
        'secret': recaptcha_secret_key,
        'response': request.form.get('g-recaptcha-response', ""),  # token from client-side
        'remoteip': request.remote_addr,
    }
    verify_response = requests.post(recaptcha_url, data=payload)
    if verify_response.status_code != 200:
        return render_template("fail.html")
    else:
        result = verify_response.json()
        success = result['success']
        if success is True:
            return render_template("success.html")
        else:
            return render_template("fail.html")


if __name__ == "__main__":
    app.run(port=5000)
