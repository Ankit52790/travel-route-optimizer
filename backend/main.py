from fastapi import FastAPI, HTTPException
from backend.genetic_algorithm import genetic_algorithm
from backend.osrm_api import get_route
  # Make sure this function exists
import logging
import sys
sys.path.append("./backend")
# Initialize FastAPI app
app = FastAPI()

# Setting up logging to capture errors
logging.basicConfig(level=logging.INFO)

@app.get("/")
def home():
    return {"message": "Travel Route Optimizer API is running"}

@app.get("/optimize-route")
def optimize_route():
    try:
        logging.info("Running optimization algorithm")
        
        # Call the genetic algorithm to get the best route
        best_route = genetic_algorithm()
        logging.info(f"Best route from genetic algorithm: {best_route}")

        # Check if the best_route is empty or has less than two locations
        if not best_route or len(best_route) < 2:
            logging.error(f"Invalid route data: {best_route}")
            raise HTTPException(status_code=400, detail="Invalid route data returned from the genetic algorithm.")

        distances = []
        total_distance = 0
        total_time = 0

        # Calculate the route details
        for i in range(len(best_route) - 1):
            logging.info(f"Fetching route between {best_route[i]} and {best_route[i + 1]}")
            dist, time = get_route(best_route[i], best_route[i + 1])

            if dist is None or time is None:
                logging.error(f"Error fetching route data for {best_route[i]} to {best_route[i + 1]}")
                raise HTTPException(status_code=500, detail=f"Error fetching route data for {best_route[i]} to {best_route[i + 1]}")

            distances.append({
                "from": best_route[i],
                "to": best_route[i + 1],
                "distance_km": dist,
                "time_min": time
            })
            total_distance += dist
            total_time += time

        return {"optimized_route": best_route, "total_distance_km": total_distance, "total_time_min": total_time, "route_details": distances}
    
    except Exception as e:
        logging.error(f"Error in optimize_route: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
