# MetroNavigator Web Application

## Overview

MetroNavigator is a web application designed to help users navigate the metro system efficiently. It provides pathfinding and visualization features using Dijkstra's algorithm, allowing users to find the best routes between stations.

## Features

- **Pathfinding:** Quickly find the shortest path between any two metro stations.
- **Journey Details:** Provides information on journey duration, distance, and necessary interchanges.
- **Metro Map Visualization:** Visualize the metro network and highlighted paths between stations.
- **Interactive Interface:** User-friendly interface for easy navigation and selection of stations.

## Technologies Used

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Graph Visualization:** NetworkX, Matplotlib
- **Database:** SQLite (db.sqlite3)
- **Deployment:** Glitch (Node.js server for running Django)

## Installation

1. **Clone the repository:**

```
git clone https://github.com/deekshith0509/MetroNavigator-WebApp.git
cd MetroNavigator-WebApp
```
2. **Set up a virtual environment (optional but recommended):**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3.**Install dependencies:**
```
pip install -r requirements.txt
```
4.**Run the Django development server:**
```
python manage.py runserver
```
5.**Access the application:** Open your browser and go to 
http://127.0.0.1:8000.

## Usage
1. Select your starting station and destination.
2. Click on "Find Path" to view the recommended route.
3. Visualize the metro map and follow the highlighted path.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.
License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Acknowledgements
```
Special thanks to the contributors of Django and NetworkX for their amazing libraries.

```
