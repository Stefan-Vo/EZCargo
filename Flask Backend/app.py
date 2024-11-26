from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS for requests from React

app = Flask(__name__)
CORS(app)  # Allow requests from different origins

@app.route('/submit-comment', methods=['POST'])
def submit_comment():
    try:
        # Parse the JSON data from the request
        data = request.get_json()
        comment = data.get('comment', '').strip()

        if not comment:
            return jsonify({"error": "Comment cannot be empty."}), 400

        # Save the comment to a file
        with open("comments.txt", "a") as file:
            file.write(comment + "\n")

        return jsonify({"message": "Comment saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)