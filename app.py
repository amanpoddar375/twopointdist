from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiYW1hbnBvZGRhciIsImEiOiJjbGt0OTljeXowNXpuM3FsMG11dTRqYXZoIn0.X_JKUIoVDvdv87SF9fM-ww"

def geocode_place(place):
    geocoding_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{place}.json"
    params = {"access_token": MAPBOX_ACCESS_TOKEN}
    response = requests.get(geocoding_url, params=params)
    data = response.json()

    if data.get("features"):
        coordinates = data["features"][0]["geometry"]["coordinates"]
        return coordinates
    else:
        return None

def calculate_distance(origin, destination):
    origin_coords = geocode_place(origin)
    dest_coords = geocode_place(destination)

    if origin_coords and dest_coords:
        directions_url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{origin_coords[0]},{origin_coords[1]};{dest_coords[0]},{dest_coords[1]}"
        params = {"access_token": MAPBOX_ACCESS_TOKEN}
        response = requests.get(directions_url, params=params)
        data = response.json()

        if data.get("routes"):
            distance = data["routes"][0]["distance"] / 1000  # Distance in kilometers
            return distance
    return None

@app.route('/calculate_distance', methods=['POST'])
def get_distance():
    data = request.json
    origin = data.get('origin')
    destination = data.get('destination')

    if origin and destination:
        distance = calculate_distance(origin, destination)
        if distance is not None:
            return jsonify({"distance": distance})
    return jsonify({"error": "Unable to calculate distance"})

if __name__ == '__main__':
    app.run()
