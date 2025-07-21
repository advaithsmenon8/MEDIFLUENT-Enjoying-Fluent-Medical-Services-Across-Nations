from flask import Blueprint, render_template, jsonify
import requests

# Create the blueprint with the correct template folder path
location_bp = Blueprint('location', __name__, 
                       template_folder='templates')

def get_nearby_hospitals(lat, lng, api_key, radius=20000):
    endpoint = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': f'{lat},{lng}',
        'radius': radius,
        'type': 'hospital',
        'key': api_key
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

def get_hospital_details(hospital_id, api_key):
    details_endpoint = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': hospital_id,
        'key': api_key
    }
    
    response = requests.get(details_endpoint, params=params)
    if response.status_code == 200:
        return response.json().get('result', {})
    else:
        return {}

def get_travel_distance(user_coords, hospitals, api_key):
    travel_distances = []
    origins = f"{user_coords[0]},{user_coords[1]}"
    destinations = "|".join(
        [f"{hospital['geometry']['location']['lat']},{hospital['geometry']['location']['lng']}" 
         for hospital in hospitals]
    )
    
    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        'origins': origins,
        'destinations': destinations,
        'mode': 'driving',
        'key': api_key
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        distances = response.json().get('rows', [])[0].get('elements', [])
        for i, hospital in enumerate(hospitals):
            distance_data = distances[i].get('distance')
            if distance_data and distances[i].get('status') == 'OK':
                distance_text = distance_data.get('text', 'Distance not available')
                distance_value = distance_data.get('value', float('inf'))
                if distance_value <= 20000:  # Only consider hospitals within 20 km
                    travel_distances.append({
                        'name': hospital['name'],
                        'travel_distance': distance_text,
                        'distance_value': distance_value,
                        'place_id': hospital['place_id']
                    })
            else:
                travel_distances.append({
                    'name': hospital['name'],
                    'travel_distance': 'Distance not available',
                    'distance_value': float('inf'),
                    'place_id': hospital['place_id']
                })
    
    travel_distances.sort(key=lambda x: x['distance_value'])
    return travel_distances

@location_bp.route('/')
def location_page():
    return render_template('index_loc.html')

@location_bp.route('/get_hospitals/<float:lat>/<float:lng>')
def get_hospitals(lat, lng):
    api_key = 'AIzaSyBf2mm-DAhXmWTWyisOlwz_rC1IcJhZtEM'  # Your API key
    hospitals = get_nearby_hospitals(lat, lng, api_key)

    user_coords = (lat, lng)
    hospitals_with_distances = get_travel_distance(user_coords, hospitals, api_key)

    response_data = []
    for hospital in hospitals_with_distances:
        details = get_hospital_details(hospital['place_id'], api_key)
        contact_number = details.get('formatted_phone_number', 'Phone number not available')
        response_data.append({
            'name': hospital['name'],
            'travel_distance': hospital['travel_distance'],
            'phone_number': contact_number
        })

    return jsonify(response_data)