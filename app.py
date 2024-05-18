from flask import Flask, request, jsonify
from services.summary import create_summary
from utils.unit_converter import get_multiple_units

app = Flask(__name__)


@app.route('/api/observation/summary', methods=['POST'])
def create_observation_summary():
    try:
        data = request.get_json()
        observations_with_multiple_units = get_multiple_units(data["entry"])

        summaries = list(map(lambda observation:
                             create_summary(observation, observations_with_multiple_units), data["entry"]))
        return jsonify({"message": "Observations summaries retrieved successfully.", "data": summaries}), 200
    except Exception as e:
        return jsonify({"message": f"Error while retrieving observation data.", "error": str(e)}), 500


if __name__ == '__main__':
    app.run()
