import streamlit as st
import requests

st.title("🚗 Travel Route Optimizer")

if st.button("Find Optimized Route"):
    try:
        # Sending a request to the FastAPI backend
        response = requests.get("http://127.0.0.1:8000/optimize-route")
        
        # Raise HTTPError for bad responses (non-2xx status codes)
        response.raise_for_status()

        if response.status_code == 200:
            # If the request is successful, extract and display the data
            data = response.json()
            st.write(f"Total Distance: {data['total_distance_km']} km")
            st.write(f"Total Time: {data['total_time_min']} minutes")
            st.write("Route Details:")
            for segment in data["route_details"]:
                st.write(f"🛤 From: {segment['from']} -> {segment['to']} ({segment['distance_km']} km, {segment['time_min']} min)")
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        # Handle any request-related exceptions (e.g., network issues)
        st.error(f"Error fetching data: {e}")
