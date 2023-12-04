# frontend/app.py

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def fetch_backend_result(username, repository, token):
    backend_url = "http://127.0.0.1:5001/api/productivity"  # Update the URL if the backend is hosted elsewhere
    payload = {
        "github_username": username,
        "github_repository": repository,
        "github_token": token,
    }

    response = requests.post(backend_url, json=payload)
    print(response.text)
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        github_username = request.form['github_username']
        github_repository = request.form['github_repository']
        github_token = request.form['github_token']

        result = fetch_backend_result(github_username, github_repository, github_token)

    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
