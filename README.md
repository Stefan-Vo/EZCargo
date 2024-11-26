# Project Description

## Frameworks Used

### Flask
- API endpoints (e.g., routes for data submission and retrieval).
- Serving static files (if needed, like a bundled React app).
- Flask creates a REST API that React (frontend) can call using HTTP requests.
-API endpoints are defined in Flask, e.g., /run-algorithm or /submit-comment.
### Axios
- For API calls
- Simplifies making API calls (GET, POST, PUT, DELETE) for Flask backend.
### React
- Frontend for User Interface
- React communicates with Flask by sending requests to Flask’s API endpoints.
## EZCargo 🚢

EZCargo is a cutting-edge system designed to simplify and optimize cargo operations for shipping companies. Whether it’s loading, unloading, or ensuring proper balance, EZCargo ensures efficiency, safety, and compliance with industry standards.

extra pip installs:
pip install flask-cors (For Connecting Flask and React)

## Primary Tasks:
Loading and Unloading Containers: Allow operators to ask for an "optimal sequence of moves."
Balancing: Provide an algorithm to balance the ship's load, ensuring the left and right sides differ by no more than 10%.
Separation of Operations:
Ensure that load/unload and balance are distinct operations and cannot occur simultaneously.
