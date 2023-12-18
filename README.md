
README - Image Frame API with MongoDB Storage
This repo contains the source code for a Flask API that retrieves and processes image frames based on depth values from a CSV file. The processed frames are stored in MongoDB and returned as base64 encoded strings.

Installation and Setup
Clone the repository.
Install required dependencies: pip install -r requirements.txt
(Optional) Configure environment variables in your system or cloud service (e.g., Heroku) for:
MONGODB_URI: Connection string for your MongoDB database.

Usage:
The API offers a single endpoint: /frames.

Request format (POST):

{
  "depth_min": float,
  "depth_max": float
}

Response format:

{
  "depths": [list of depth values],
  "pixels": [list of base64 encoded image data]
}

Example usage:

curl -X POST http://localhost:5000/frames -H "Content-Type: application/json" -d '{"depth_min": 10.0, "depth_max": 20.0}'

This will retrieve image frames for depths between 10.0 and 20.0, process them, store them in MongoDB, and return the base64 encoded image data and corresponding depth values in the JSON response.

API Deployment
This API can be deployed on various platforms, including:

Locally: Run python app.py to start the API server on your local machine.
Heroku: Follow the Heroku deployment guide for Flask apps and set environment variables for MongoDB connection.
Cloud platforms: Follow the specific deployment instructions for your chosen cloud platform.
Remember to adjust firewall rules and access controls based on your security requirements.

Additional Notes
This API uses MongoDB for image storage. Consider alternative storage solutions based on your needs.
The current code serves as a basic example and can be extended with additional features like user authentication, different image formats, etc.
Refer to the code comments for specific functionality details.
Feel free to contribute to this project or propose improvements by raising issues or pull requests.

Contributing
Fork the repository.
Create a new branch for your changes.
Implement your changes and add relevant documentation.
Submit a pull request to the main repository.
