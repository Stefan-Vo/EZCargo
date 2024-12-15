from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS  
from operators import balanceContainers, Cell, Buffer
from container import Container
from copy import deepcopy
from ship import ship
import numpy as np
import os
from werkzeug.utils import secure_filename
import re


app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5000"],  
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)



# Create comments.txt if it doesn't exist
if not os.path.exists('comments.txt'):
    open('comments.txt', 'w').close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/submit-comment', methods=['POST'])
def submit_comment():
    try:
        data = request.get_json()
        comment_text = data.get('text', '').strip()
        timestamp = data.get('timestamp', '')

        if not comment_text:
            return jsonify({"error": "Comment cannot be empty."}), 400

        # Save comment
        with open("comments.txt", "a") as file:
            file.write(f"{timestamp} - {comment_text}\n")

        return jsonify({
            "message": "Comment saved successfully!"
        }), 200

    except Exception as e:
        print(f"Error in submit_comment: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/get-comments')
def get_comments():
    try:
        comments = []
        with open("comments.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    # Split the line at the first occurrence of " - "
                    parts = line.split(" - ", 1)
                    if len(parts) == 2:
                        timestamp, text = parts
                        comments.append({
                            "timestamp": timestamp,
                            "text": text
                        })
        return jsonify(comments), 200
    except FileNotFoundError:
        return jsonify([]), 200
    except Exception as e:
        print(f"Error in get_comments: {str(e)}")
        return jsonify({"error": str(e)}), 500




@app.route('/balance', methods=['POST'])
def balance_endpoint():
    try:
        # Check if file-based containers are requested
        use_uploaded_file = request.get_json().get('useUploadedFile', False)
        
        # Create Ship object
        ship_matrix = np.zeros((8, 12), dtype=int)
        my_ship = ship(ship_matrix)

        # Determine how to get containers
        if use_uploaded_file:
            # Get the most recently uploaded filename
            recent_files = os.listdir(app.config['UPLOAD_FOLDER'])
            if not recent_files:
                return jsonify({"error": "No uploaded files found"}), 400
            
            # Get the most recent file (last uploaded)
            recent_filename = max(recent_files, key=lambda f: os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], f)))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], recent_filename)
            
            # Parse containers from the uploaded file
            uploaded_containers = parse_uploaded_containers(filepath)
            
            # Convert parsed containers to Cell objects
            cells = []
            for container_data in uploaded_containers:
                position = container_data['position']
                container = Container(container_data['id'], container_data['weight'])
                
                cell = Cell(
                    position=position,
                    isFilled=container.id != "UNUSED",
                    container=container
                )
                cells.append(cell)
        else:
            # Use containers from frontend grid items
            cells = []
            for item in request.get_json().get("cellList", []):
                position = (item.get("row", 1), item.get("column", 1))
                weight = item.get("weight", 0)
                name = item.get("name", "UNUSED")
                
                # Create Container object
                container = Container(name, weight)
                
                # Create Cell object
                cell = Cell(
                    position=position,
                    isFilled=name != "UNUSED",
                    container=container
                )
                cells.append(cell)

        # Create empty buffer list
        buffer = []
        for i in range(8):
            for j in range(12):
                buffer.append(Buffer(
                    position=(i+1, j+1),
                    isFilled=False,
                    container=Container("UNUSED", 0)
                ))

        # Call balance function
        result = balanceContainers(my_ship, cells, buffer)

        # Convert result back to frontend format
        response_data = []
        for cell in cells:
            response_data.append({
                "id": cell.position[0] * 12 + cell.position[1],
                "name": cell.container.id if cell.isFilled else "UNUSED",
                "weight": f"{cell.container.weight} Lbs: " if cell.isFilled else "0 Lbs: ",
                "position": cell.position
            })

        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error in balance_endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        print("Received upload request")  # Debug log
        print("Files:", request.files)  # Debug log
        
        if 'file' not in request.files:
            print("No file in request")  # Debug log
            return jsonify({"error": "No file part"}), 400
            
        file = request.files['file']
        print(f"Received file: {file.filename}")  # Debug log
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving to: {filepath}")  # Debug log
            file.save(filepath)
            
            # Return filename in response
            return jsonify({"message": "File uploaded successfully", "filename": filename}), 200
            
        return jsonify({"error": "Invalid file type"}), 400

    except Exception as e:
        print(f"Error in upload_file: {str(e)}")
        return jsonify({"error": str(e)}), 500


def parse_uploaded_containers(filepath):
    """
    Parse the uploaded container file and extract container information.
    
    :param filepath: Full path to the uploaded text file
    :return: List of container dictionaries
    """
    containers = []
    
    try:
        with open(filepath, 'r') as file:
            for line in file:
                # Use regex to parse each line
                match = re.match(r'\[(\d{2}),(\d{2})\], \{(\d{5})\}, (.+)', line.strip())
                
                if match:
                    row, col, weight, container_id = match.groups()
                    
                    # Convert row and column to 1-based indexing
                    position = (int(row), int(col))
                    
                    # Convert weight to int, handle NAN or zero weights
                    try:
                        weight_int = int(weight)
                    except ValueError:
                        weight_int = 0
                    
                    # Handle container ID, use "UNUSED" for empty or NAN containers
                    if container_id.strip() in ['NAN', 'UNUSED'] or weight_int == 0:
                        container_id = "UNUSED"
                    
                    # Create a container-like dictionary
                    containers.append({
                        'position': position,
                        'weight': weight_int,
                        'id': container_id
                    })
    
    except Exception as e:
        print(f"Error parsing containers: {e}")
        return []
    
    return containers

@app.route('/process-upload', methods=['POST'])
def process_upload():
    try:
        # Get the filename from the request
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({"error": "No filename provided"}), 400
        
        # Construct full filepath
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404
        
        # Parse containers
        containers = parse_uploaded_containers(filepath)
        
        # Prepare response data
        positions = [(i, j) for i in range(1, 9) for j in range(1, 13)]
        response_data = []
        
        for pos in positions:
            # Find matching container for this position
            matching_container = next((c for c in containers if c['position'] == pos), None)
            
            if matching_container:
                response_data.append({
                    "id": (pos[0] - 1) * 12 + pos[1],
                    "name": matching_container['id'],
                    "weight": f"{matching_container['weight']} Lbs: ",
                    "position": pos
                })
            else:
                response_data.append({
                    "id": (pos[0] - 1) * 12 + pos[1],
                    "name": "UNUSED",
                    "weight": "0 Lbs: ",
                    "position": pos
                })
        
        return jsonify(response_data), 200
    
    except Exception as e:
        print(f"Error in process_upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)