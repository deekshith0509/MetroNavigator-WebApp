from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render
from .models import Station
from .services import MetroService
def fare_chart(request):
    return render(request, 'metro/fare_chart.html')
    
def metro_map(request):
    return render(request, 'metro/metro_map.html' )





def terms_of_service(request):
    return render(request, 'metro/terms_of_service.html')

def privacy_policy(request):
    return render(request, 'metro/privacy_policy.html')
    

from django.shortcuts import render
from django.utils import timezone
import pytz
from datetime import datetime, timedelta
from .services import MetroService




@csrf_exempt
def home(request):
    stations = Station.objects.all().order_by('name')

    if request.method == 'POST':
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        mode = request.POST.get('mode', 'time')  # Default mode is 'time'

        metro_service = MetroService()
        result, error = metro_service.find_path(source, destination, mode)

        # Visualize the metro map after finding the path
        visualization_path = metro_service.visualize_metro_map(source, destination, mode)
        linear_path_details = metro_service.visualize_linear_path(result['path'])

        # Get journey details including interchange stations
        journey_details = metro_service._get_journey_details(result['path'], mode)

        # Create a list of stations with the is_necessary_interchange flag
        detailed_linear_path = []
        for station in linear_path_details:
            # Check if the station is in the interchange list
            is_necessary_interchange = station in journey_details['interchange_stations']
            detailed_linear_path.append({
                'name': station,
                'is_necessary_interchange': is_necessary_interchange
            })

        if error:
            return render(request, 'metro/home.html', {
                'stations': stations,
                'error': error,
                'visualization_path': visualization_path,
                'linear_path_details': detailed_linear_path,
                'journey_details': journey_details['journey_details'],  # Pass journey details including interchanges
            })

        # Calculate the number of stations in the path
        number_of_stations = len(result.get('path', []))  # Default to an empty list if 'path' is not found

        total_time = result.get('total_time', 0)  # Default to 0 if not found
        kolkata_tz = pytz.timezone('Asia/Kolkata')

        # Use datetime from pytz to get the current time in the specified timezone (not the local machine)
        current_time = datetime.now(kolkata_tz)  # This will use the 'Asia/Kolkata' timezone directly

        # Calculate the expected departure time
        expected_departure_time = current_time + timedelta(minutes=total_time)
        formatted_departure_time = expected_departure_time.strftime('%I:%M %p')  # 12-hour clock with AM/PM

        return render(request, 'metro/result.html', {
            'result': result,
            'stations': stations,
            'source': source,
            'destination': destination,
            'mode': mode,
            'visualization_path': visualization_path,
            'linear_path_details': detailed_linear_path,
            'journey_details': journey_details['journey_details'],  # Pass journey details including interchanges
            'now': current_time,  # Pass the datetime object directly
            'expected_departure_time': formatted_departure_time,  # Keep formatted for display
            'number_of_stations': number_of_stations,  # Pass the count of stations
        })


    return render(request, 'metro/home.html', {'stations': stations})


from django.http import JsonResponse
from .models import Station
from geopy.distance import geodesic
import json

def nearest_station(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_location = (body['latitude'], body['longitude'])

            stations = Station.objects.all()
            nearest_station = None
            shortest_distance = float('inf')

            for station in stations:
                station_location = (station.latitude, station.longitude)
                distance = geodesic(user_location, station_location).meters

                if distance < shortest_distance:
                    shortest_distance = distance
                    nearest_station = station.name

            return JsonResponse({
                'nearest_station': nearest_station,
                'distance': shortest_distance
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Missing latitude or longitude'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)
