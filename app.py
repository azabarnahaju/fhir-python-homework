from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/observation/summary', methods=['POST'])
def create_observation_summary():
    data = request.get_json()
    return jsonify(data)


if __name__ == '__main__':
    app.run()
