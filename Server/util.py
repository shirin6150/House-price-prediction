import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index>=0:
        x[loc_index] = 1

    try:
        return round(__model.predict([x])[0],2)
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        print(f"Input values: location={location}, sqft={sqft}, bhk={bhk}, bath={bath}")
        print(f"Processed input array: {x}")
        raise

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Get the current directory where util.py is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    columns_path = os.path.join(current_dir, r"C:\Users\shiri\OneDrive\Documents\VS Code\home price prj\Server\artifacts", r"C:\Users\shiri\OneDrive\Documents\VS Code\home price prj\Server\artifacts\columns.json")
    model_path = os.path.join(current_dir, r"C:\Users\shiri\OneDrive\Documents\VS Code\home price prj\Server\artifacts", r"C:\Users\shiri\OneDrive\Documents\VS Code\home price prj\Server\artifacts\banglore_home_prices_model.pickle")

    print(f"Looking for columns.json at: {columns_path}")
    print(f"Looking for model pickle at: {model_path}")

    try:
        with open(columns_path, "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk
            print(f"Loaded {len(__locations)} locations")
    except Exception as e:
        print(f"Error loading columns.json: {str(e)}")
        raise

    try:
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model file: {str(e)}")
        raise

    print("loading saved artifacts...done")

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    # Test the model with some sample predictions
    test_locations = ['1st Phase JP Nagar', 'Indira Nagar', 'Electronic City']
    for loc in test_locations:
        try:
            price = get_estimated_price(loc, 1000, 2, 2)
            print(f"Estimated price for {loc}: {price} Lakh")
        except Exception as e:
            print(f"Error predicting price for {loc}: {str(e)}")

