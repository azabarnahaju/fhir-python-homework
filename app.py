from flask import Flask, request, jsonify
from services.summary import create_summary
from utils.unit_converter import get_multiple_units

app = Flask(__name__)


@app.route('/api/observation/summary', methods=['POST'])
def create_observation_summary():
    data = request.get_json()
    observations_with_multiple_units = get_multiple_units(data["entry"])

    summaries = list(map(lambda observation:
                         create_summary(observation, observations_with_multiple_units), data["entry"]))
    return jsonify(summaries)


if __name__ == '__main__':
    app.run()
