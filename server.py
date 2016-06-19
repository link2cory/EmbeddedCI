from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/github/push/', methods = ['POST'])
def service_github_webhook():
    payload = request.form['payload']
    try:
        payload = json.loads(payload)
    except JSONDecodeError:
        return 'failure'

    return 'success!'