import requests
import json

def fetch_metro_stations():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json];
    area[name="Hyderabad"];
    node(area)["railway"="station"]["station"="subway"]["construction"!~".*"];
    out body;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Successfully fetched data from Overpass API.")
        elements = data['elements']
        print(f"Number of elements found: {len(elements)}")
        for element in elements:
            if 'tags' in element and 'name' in element['tags']:
                name = element['tags']['name']
                lat = round(element['lat'], 12)
                lon = round(element['lon'], 12)
                if "(u/c)" not in name:  # Exclude stations marked as under construction
                    print(f"Station: {name}")
                    print(f"Latitude: {lat}, Longitude: {lon}\n")
    else:
        print("Failed to fetch data from Overpass API.")

if __name__ == "__main__":
    print("Sending request to Overpass API...")
    fetch_metro_stations()
