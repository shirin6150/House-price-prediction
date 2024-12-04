from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import traceback

app = Flask(__name__)
CORS(app)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        print("Fetching location names...")
        locations = util.get_location_names()
        print(f"Locations fetched: {locations}")
        response = jsonify({
            'locations': locations
        })
        return response
    except Exception as e:
        print(f"Error in get_location_names: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.get_json()
        print("Received data:", data)
        
        # Input validation
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        required_fields = ['total_sqft', 'location', 'bhk', 'bath']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])

        # Value validation
        if total_sqft <= 0:
            return jsonify({'error': 'Square feet should be greater than 0'}), 400
        if bhk <= 0:
            return jsonify({'error': 'BHK should be greater than 0'}), 400
        if bath <= 0:
            return jsonify({'error': 'Bathrooms should be greater than 0'}), 400

        print(f"Processing: sqft={total_sqft}, location={location}, bhk={bhk}, bath={bath}")
        
        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        print("Estimated price:", estimated_price)
        
        return jsonify({
            'estimated_price': estimated_price
        })
        
    except ValueError as ve:
        print(f"Value error: {str(ve)}")
        return jsonify({'error': f'Invalid value: {str(ve)}'}), 400
    except Exception as e:
        print("Error occurred:", str(e))
        print("Traceback:", traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    try:
        util.load_saved_artifacts()
        print("Artifacts loaded successfully")
        app.run(debug=True)
    except Exception as e:
        print(f"Failed to start server: {str(e)}")