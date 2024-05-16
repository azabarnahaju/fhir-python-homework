from flask import Flask, request, jsonify
from services.summary import create_summary

app = Flask(__name__)


@app.route('/api/observation/summary', methods=['POST'])
def create_observation_summary():
    data = request.get_json()

    summaries = list(map(lambda observation: create_summary(observation), data["entry"]))
    return jsonify(summaries)


if __name__ == '__main__':
    app.run()
