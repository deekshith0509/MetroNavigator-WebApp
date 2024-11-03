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

from datetime import datetime, timedelta
import pytz
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

        if error:
            return render(request, 'metro/home.html', {
                'stations': stations,
                'error': error,
                'visualization_path': visualization_path
            })

        # Access total_time correctly from the result dictionary
        total_time = result.get('total_time', 0)  # Default to 0 if not found
        
        # Get the current time in Kolkata timezone
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(kolkata_tz)

        # Calculate expected departure time by adding total_time minutes
        expected_departure_time = current_time + timedelta(minutes=total_time)

        # Format the expected departure time for display
        formatted_departure_time = expected_departure_time.strftime('%I:%M %p')  # Format to 12-hour clock with AM/PM

        # Render the result page with journey details
        return render(request, 'metro/result.html', {
            'result': result,
            'stations': stations,
            'source': source,
            'destination': destination,
            'mode': mode,
            'visualization_path': visualization_path,
            'now': current_time,  # Pass the datetime object directly
            'expected_departure_time': formatted_departure_time,  # Keep formatted for display
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
