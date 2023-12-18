import numpy as np
import cv2
from flask import Flask, request, jsonify
import csv
import pymongo
import base64
import pandas as pd
from pymongo.mongo_client import MongoClient

# MongoDB connection details
MONGO_URI = "mongodb+srv://nbamne3:qSR4ydc2bBFfleAq@cluster0.o4vw2qa.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "images"
COLLECTION_NAME = "frames"
# uri = "mongodb+srv://nbamne3:qSR4ydc2bBFfleAq@cluster0.o4vw2qa.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(MONGO_URI)
# Define custom colormap
cmap = cv2.COLORMAP_JET

# Create Flask app
app = Flask(__name__)

# Function to read image data from CSV
def read_image_data(depth_min, depth_max):
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        df = pd.read_csv('./data/img.csv')
        filtered_df = df[(df["depth"] >= depth_min) & (df["depth"] <= depth_max)]

        images_data = []
        for index, row in filtered_df.iterrows():
            depth = row['depth']
            pixels = row.iloc[1:].values.astype('uint8')
            image = pixels.reshape((1, -1, 1))
            images_data.append({'depth': depth, 'pixels': image})

        return images_data
    except FileNotFoundError:
        return {"error": "Csv file not found"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


# Function to resize and apply colormap
def process_image(image_data):
    try:
        resized_image = cv2.resize(image_data['pixels'], (150, 150))
        colored_image = cv2.applyColorMap(resized_image, cmap)
        return colored_image
    except Exception as e:
        return {"error": f"Image processing error: {e}"}


# Function to store image in database
def store_image(depth, processed_image):
    # Connect to MongoDB
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Prepare image data for storage
    encoded_image = base64.b64encode(cv2.imencode(".jpg", processed_image)[1]).decode()

    # Store image in database
    collection.insert_one({"depth": depth, "image": encoded_image})

    # Close connection
    client.close()


# API route to retrieve image frames
@app.route("/frames", methods=["POST"])
def get_frames():
    try:
        dataDict = request.get_json()
        
        depth_min = float(dataDict["depth_min"])
        depth_max = float(dataDict["depth_max"])
        
        if(depth_min < 0 or depth_max < 0):
            raise Exception('depth_min and depth_max shloud be greater than 0')

        image_data = read_image_data(depth_min, depth_max)
        if "error" in image_data:
            return jsonify(image_data)

        image_frames = []
        depths = []
        for data in image_data:
            processed_image = process_image(data)
            if "error" in processed_image:
                return jsonify( )

            image_frames.append(processed_image)
            depths.append(data['depth'])
            store_image(data['depth'], processed_image)

        image_data_base64 = [base64.b64encode(cv2.imencode(".jpg", frame)[1]).decode() for frame in image_frames]

        return jsonify({"depths": depths, "pixels": image_data_base64}), 200
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {e}"}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)