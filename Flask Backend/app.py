from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/run-algorithm', methods=['POST'])
def run_algorithm():
    # Example algorithm
    data = request.json
    result = {"output": sum(data['numbers'])}  # Example algorithm: summing numbers
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)