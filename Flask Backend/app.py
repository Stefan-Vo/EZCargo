from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from operators import balanceContainers  # Assuming this function exists in your 'operators.py'

app = Flask(__name__)
CORS(app)

# Upload folder setup (make sure it exists)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        # Check if a file is part of the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        # Check if the file is empty
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Save the file to the server
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        return jsonify({"message": f"File {file.filename} uploaded successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-manifest', methods=['GET'])
def get_manifest():
    try:
        # Read the content of the manifest.txt file
        manifest_path = os.path.join(UPLOAD_FOLDER, 'manifest.txt')
        
        if not os.path.exists(manifest_path):
            return jsonify({"error": "manifest.txt not found"}), 404

        with open(manifest_path, 'r') as file:
            manifest_content = file.read()

        return jsonify({"data": manifest_content}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/create-container-file', methods=['POST'])
def create_container_file():
    try:
        # Get the containers data from the request
        containers = request.json.get("containers", [])
        
        if not containers:
            return jsonify({"error": "No container data provided"}), 400
        
        # Define the file name
        filename = 'containers.txt'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Open the file in append mode
        with open(file_path, 'a') as f:
            for container in containers:
                # Append container name and weight to the file
                container_data = f"Name: {container['name']}, Weight: {container['weight']}\n"
                f.write(container_data)
        
        return jsonify({"message": "Containers added to file successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/balance', methods=['POST'])
def balance_endpoint():
    try:
        data = request.get_json()
        print("Received Data:", data)

        # Extract input data
        ship = data.get("ship")
        cellList = data.get("cellList", [])
        bufferList = data.get("bufferList", [])
        print("Ship:", ship)
        print("CellList:", cellList)
        print("BufferList:", bufferList)

        if not ship or not cellList or not bufferList:
            return jsonify({"error": "Missing required parameters"}), 400

        # Call the function to perform the balance calculation
        result = balanceContainers(ship, cellList, bufferList)
        print("Balance Result:", result)

        return jsonify(result), 200
    except Exception as e:
        print("Error in /balance endpoint:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
