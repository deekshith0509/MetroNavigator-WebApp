from django.shortcuts import render
from .models import Station
from .services import MetroService
def fare_chart(request):
    return render(request, 'metro/fare_chart.html')
    
def metro_map(request):
    return render(request, 'metro/metro_map.html' )
def home(request):
    # Get all stations ordered by name for dropdown or selection
    stations = Station.objects.all().order_by('name')

    if request.method == 'POST':
        # Get source, destination, and mode from the form submission
        source = request.POST.get('source')
        destination = request.POST.get('destination')
        mode = request.POST.get('mode', 'time')  # Default mode is 'time'

        # Initialize the MetroService to find the path
        metro_service = MetroService()
        result, error = metro_service.find_path(source, destination, mode)

        # Visualize the metro map after finding the path
        visualization_path = metro_service.visualize_metro_map(source, destination, mode)

        if error:
            # Render the home page with an error message
            return render(request, 'metro/home.html', {
                'stations': stations,
                'error': error,
                'visualization_path': visualization_path
            })

        # Render the result page with journey details
        return render(request, 'metro/result.html', {
            'result': result,
            'stations': stations,
            'source': source,
            'destination': destination,
            'mode': mode,
            'visualization_path': visualization_path
        })

    # Render the home page for GET requests
    return render(request, 'metro/home.html', {'stations': stations})
