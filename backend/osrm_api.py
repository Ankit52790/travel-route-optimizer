from backend import requests
import logging

# Setting up logging
logging.basicConfig(level=logging.INFO)

# Fetch optimized travel distance using OpenStreetMap API
def get_route(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=false"
    
    try:
        logging.info(f"Fetching route from {start} to {end}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        data = response.json()

        # Check if the expected route data exists
        if 'routes' in data and len(data['routes']) > 0:
            distance = data['routes'][0]['distance'] / 1000  # Convert meters to km
            duration = data['routes'][0]['duration'] / 60  # Convert seconds to minutes
            logging.info(f"Route found: Distance = {distance:.2f} km, Duration = {duration:.2f} minutes")
            return distance, duration
        else:
            logging.error("Error: No route found.")
            return None, None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None, None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None, None

# Example usage
if __name__ == "__main__":
    start = (28.7041, 77.1025)  # Delhi
    end = (19.0760, 72.8777)    # Mumbai
    dist, dur = get_route(start, end)
    if dist is not None and dur is not None:
        print(f"Distance: {dist:.2f} km, Duration: {dur:.2f} minutes")
    else:
        print("Failed to fetch the route data.")
