@echo off
echo Starting Django servers in the background...

:: Get the local network IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /R "IPv4.*192\."') do set IP=%%a
set IP=%IP:~1%

REM Start city_selector server and store PID
start /b python C:\Users\deeks\Desktop\Projects\metro\city_selector\manage.py runserver 0.0.0.0:8000
echo %! > city_selector.pid

REM Wait for 5 seconds before starting the next server
timeout /t 5 >nul

REM Start Hyderabad server and store PID
start /b python C:\Users\deeks\Desktop\Projects\metro\hyderabad\manage.py runserver_plus 0.0.0.0:8001 --cert-file cert.pem --key-file key.pem
echo %! > hyderabad.pid

REM Wait for 5 seconds before starting the next server
timeout /t 5 >nul

REM Start Kochi server and store PID
start /b python C:\Users\deeks\Desktop\Projects\metro\kochi\manage.py runserver_plus 0.0.0.0:8002 --cert-file cert.pem --key-file key.pem
echo %! > kochi.pid

echo All servers started successfully!

REM Wait for user to press Ctrl+C
echo Press Ctrl+C to stop all servers...
:loop
echo http://%IP%:8000
timeout /t 4 >nul
goto loop
