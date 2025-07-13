import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
from exa_py import Exa
import os

api_511_key = os.getenv("511APIKEY")
api_transitland_key = os.getenv("TRANSITLAND_API_KEY")
api_exa_key = os.getenv("EXA_SEARCH_API_KEY")
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

def get_geolocation(api_key):
    """
    Call the Google Maps Geolocation API to get the device's location.
    """
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}"
    
    # Example payload (you can customize this based on available data)
    payload = {
        "considerIp": True,  # Use the device's IP address for location
        "wifiAccessPoints": [
            {
                "macAddress": "01:23:45:67:89:AB",
                "signalStrength": -65,
                "signalToNoiseRatio": 40
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()
        lat = data.get("location", {}).get("lat")
        lng = data.get("location", {}).get("lng")

        return [lat, lng]  # Return the latitude and longitude as a list
    except requests.RequestException as e:
        return f"Error calling Geolocation API: {e}"

class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    option: str = Field(..., description="The type of data to fetch (e.g., routes, stops).")
    search: str = Field(..., description="Search query for routes or stops.")
    route_type: int = Field(..., description="Type of route to filter by...", ge=0, le=12)

class transitlandAPICaller(BaseTool):
    name: str = "TransitLand API Caller"
    description: str = (
        "A tool for interacting with the TransitLand API to fetch transit data."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, option: str, search: str, route_type: int) -> str:
        # Implementation goes here
        """Fetches data from the TransitLand API based on the provided option and agency or query.
        args:
            option (str): The type of data to fetch (e.g., routes, stops).
            search (str): The search query for routes or stops.
        """
        list_of_them = []

        if option == "routes":
            api_url = f"https://transit.land/api/v2/rest/routes?api_key=x5unflDSbpKEWnThyfmteM8MHxIsg3eL"
            params = {"search": search, "route_type": route_type} if search else {"route_type": route_type}
        elif option == "stops":
            api_url = f"https://transit.land/api/v2/rest/stops?api_key=x5unflDSbpKEWnThyfmteM8MHxIsg3eL"
            params = {"search": search, "served_by_route_type": route_type} if search else {"served_by_route_type": route_type}
        else:
            return "Invalid option"

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an error for HTTP errors

            if option == "routes":
                routes = json.loads(response.text).get("routes", [])  # Extract the "routes" key from the JSON response
                for router in routes:
                    list_of_them.append(f"{router.get('route_short_name', 'N/A')} - {router.get('route_long_name', 'N/A')}")

                return list_of_them if list_of_them else "No routes found for the given query."
            elif option == "stops":
                stops = json.loads(response.text).get("stops", [])
                for stop in stops:
                    list_of_them.append(f"{stop.get('stop_name', 'N/A')} - {stop.get('stop_id', 'N/A')}")

                return list_of_them if list_of_them else "No stops found for the given query."
        except requests.RequestException as e:
            return f"Error fetching data: {e}"

class ExaSearchToolInput(BaseModel):
    """Input schema for ExaSearchTool."""
    query: str = Field(..., description="The search query to know more info about transit agencies.")

class ExaSearchTool(BaseTool):
    name: str = "Exa Search Tool"
    description: str = (
        "A tool for searching and retrieving information about transit agencies using Exa search."
    )
    args_schema: Type[BaseModel] = ExaSearchToolInput

    def _run(self, query: str) -> str:
        # Implementation goes here
        """Searches for transit agencies using Exa search.
        args:
            query (str): The search query to find transit agencies.
        """
        if query == "N/A":
            return "Skip this."

        exa = Exa(api_key=api_exa_key)
        typeIN = exa.search_and_contents(query, text=True).results
        return typeIN if typeIN else "No results found for the given query."
    
class NearbyTransitToolInput(BaseModel):
    """Input schema for NearbyTransitTool."""
    radius: int = Field(..., description="The radius in meters to search for nearby transit options.")
    option: str = Field(..., description="The type of data to fetch (e.g., routes, stops).")

class NearbyTransitTool(BaseTool):
    name: str = "Nearby Transit Tool"
    description: str = (
        "A tool for finding nearby transit options based on location and radius."
    )
    args_schema: Type[BaseModel] = NearbyTransitToolInput

    def _run(self, radius: int, option: str) -> str:
        # Implementation goes here
        """Finds nearby transit options based on location and radius.
        args:
            option (str): The type of data to fetch (e.g., routes, stops).
            radius (int): The radius in meters to search for nearby transit options.
        """
        lat, lng = get_geolocation(google_maps_api_key)
        list_of_them = []

        if option == "routes":
            api_url = f"https://transit.land/api/v2/rest/routes?api_key={api_transitland_key}"
            params = {"lat": lat, "lon": lng, "radius": radius}
        elif option == "stops":
            api_url = f"https://transit.land/api/v2/rest/stops?api_key={api_transitland_key}"
            params = {"lat": lat, "lon": lng, "radius": radius}
        else:
            return "Invalid option"

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an error for HTTP errors

            if option == "routes":
                routes = json.loads(response.text).get("routes", [])  # Extract the "routes" key from the JSON response
                for router in routes:
                    list_of_them.append(f"{router.get('route_short_name', 'N/A')} - {router.get('route_long_name', 'N/A')}")

                return list_of_them if list_of_them else "No routes found for the given query."
            elif option == "stops":
                stops = json.loads(response.text).get("stops", [])
                for stop in stops:
                    list_of_them.append(f"{stop.get('stop_name', 'N/A')} - {stop.get('stop_id', 'N/A')}")

                return list_of_them if list_of_them else "No stops found for the given query."
        except requests.RequestException as e:
            return f"Error fetching data: {e}"

class TrafficDataTool(BaseTool):
    name: str = "Traffic Data Tool"
    description: str = (
        "A tool for fetching real-time traffic data for a specific location."
    )

    def _run(self) -> str:
        # Implementation goes here
        """Fetches real-time traffic data for a specific location.
        args:
            location (str): The location to fetch traffic data for.
        """
        list_of_incidents = []
        apiUrl = f"https://api.511.org/traffic/events?api_key={api_511_key}&format=JSON"
        
        try:
            response = requests.get(apiUrl)
            response.raise_for_status()  # Raise an error for HTTP errors
            traffic_data = json.loads(response.content.decode("utf-8-sig")).get("events", [])

            if traffic_data:
                for incident in traffic_data:
                    highway = incident.get('roads', [{}])[0].get('name')
                    self.new_method(list_of_incidents, incident, highway)

                return list_of_incidents if list_of_incidents else "No traffic incidents found."
            else:
                return "No traffic incidents found."
        except requests.RequestException as e:
            return f"Error fetching traffic data: {e}"

    def new_method(self, list_of_incidents, incident, highway):
        list_of_incidents.append(f"Incident: {incident.get('headline')}, Highway: {highway}")
        
class TransitDeparturesToolInput(BaseModel):
    """Input schema for TransitDeparturesTool."""
    stop_id: str = Field(..., description="The ID of the transit stop to get departures from.")
    agency_onestop_id: str = Field(..., description="The Onestop ID of the transit agency to get departures from.")

class TransitDeparturesTool(BaseTool):
    name: str = "Transit Departures Tool"
    description: str = (
        "A tool for fetching upcoming departures for a specific transit stop."
    )

    def _run(self, stop_id: str, agency_onestop_id: str) -> str:
        # Implementation goes here
        """Fetches upcoming departures for a specific transit stop.
        args:
            stop_id (str): The ID of the transit stop to get departures from. Required.
            agency_onestop_id (str): The Onestop ID of the transit agency to get departures from. Don't confuse it with the stop_id. Required.
        """
        all_departures = []
        if stop_id == "N/A" and agency_onestop_id == "N/A":
            return "Skip this."

        apiUrl = f"https://transit.land/api/v2/rest/stops?stop_id={stop_id}&served_by_onestop_ids={agency_onestop_id}&api_key={api_transitland_key}"
        try:
            response = requests.get(apiUrl)
            response.raise_for_status()  # Raise an error for HTTP errors
            data = json.loads(response.text).get("stops", [])
            onestop_departures_id = data[0].get("onestop_id") if data else None

            apiUrlDepartures = f"https://transit.land/api/v2/rest/stops/{onestop_departures_id}/departures?api_key={api_transitland_key}"
            try:
                response = requests.get(apiUrlDepartures)
                response.raise_for_status()
                departures_data = json.loads(response.text).get("stops", [])
                departures_data_two = departures_data[0].get("departures", []) if departures_data else []

                for departure in departures_data_two:
                    # print(departure)
                    arrivals = departure.get("arrival")
                    estimated = arrivals.get("estimated")
                    trip = departure.get("trip")
                    route = trip.get("route")
                    route_name = route.get("route_short_name") if route else "N/A"
                    trip_headsign = trip.get("trip_headsign") if trip else "N/A"
                    all_departures.append(f'{route_name} to {trip_headsign} at {estimated}')

                return all_departures if all_departures else "No departures found for the given stop."
            except requests.RequestException as e:
                return f"Error fetching departure data: {e}"
        except requests.RequestException as e:
            return f"Error fetching departure data: {e}"