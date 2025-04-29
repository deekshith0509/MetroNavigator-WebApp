import socket
from django.shortcuts import redirect, render

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "127.0.0.1"  # Fallback in case of error
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def select_city(request):
    local_ip = get_local_ip()  # Get dynamic local network IP

    if request.method == "POST":
        city = request.POST.get("city")
        if city == "hyderabad":
            return redirect(f"https://{local_ip}:8001/")  # Redirect to Hyderabad's Django server
        elif city == "kochi":
            return redirect(f"https://{local_ip}:8002/")  # Redirect to Kochi's Django server

    return render(request, "city_selector/select_city.html")
