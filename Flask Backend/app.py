from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS  
from operators import balanceContainers

app = Flask(__name__)
CORS(app)  

@app.route('/submit-comment', methods=['POST'])
def submit_comment():
    try:
        # Parse the JSON data from the request from axios
        data = request.get_json()
        comment = data.get('comment', '').strip()

        if not comment:
            return jsonify({"error": "Comment cannot be empty."}), 400

        # Save the comment to comment.txt prob change to manifest.txt later  file
        with open("comments.txt", "a") as file:
            file.write(comment + "\n")

        return jsonify({"message": "Comment saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-comments')
def get_comments():
    # Assuming Flask Backend is the current working directory
    return send_from_directory('.', 'comments.txt')

@app.route('/get-file', methods=['GET'])
def get_file():
    return send_file('comments.txt', as_attachment=False)  # Set `as_attachment=True` to force a download




@app.route('/balance', methods=['POST'])
def balance_endpoint():
    try:
        data = request.get_json()

        # Extract input data
        ship = data.get("ship")
        cellList = data.get("cellList", [])
        bufferList = data.get("bufferList", [])

        if ship is None or cellList is None or bufferList is None:
            return jsonify({"error": "Missing required parameters"}), 400

        result = balanceContainers(ship, cellList, bufferList)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)