import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import os

import os
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for rendering
import matplotlib.pyplot as plt

from collections import defaultdict
import heapq
import networkx as nx
import matplotlib.pyplot as plt
import os
from .models import Station, Connection


PLATFORM_MAPPING = {
        ('blue', 'interchange'): 1,
        ('interchange', 'blue'): 2,
    }



class PathSegment:
    def __init__(self, station, time, distance):
        self.station = station
        self.time = time
        self.distance = distance

class MetroService:

    def __init__(self):
        self._initialize_graph()

    def _initialize_graph(self):
        self.metro_map = defaultdict(list)
        self.stations = {station.name: station for station in Station.objects.all()}

        connections = Connection.objects.select_related('from_station', 'to_station').all()
        for conn in connections:
            self.metro_map[conn.from_station.name].append(
                PathSegment(conn.to_station.name, conn.time, conn.distance)
            )
            self.metro_map[conn.to_station.name].append(
                PathSegment(conn.from_station.name, conn.time, conn.distance)
            )



    def _get_journey_details(self, path, mode):
        journey_details = []
        total_distance = 0
        total_time = 0

        # Initialize with the line of the first station
        current_line = self.stations[path[0]].line_color

        for i in range(len(path) - 1):
            from_station = path[i]
            to_station = path[i + 1]

            segment = next(
                seg for seg in self.metro_map[from_station]
                if seg.station == to_station
            )

            from_line = self.stations[from_station].line_color
            to_line = self.stations[to_station].line_color

            # Check if the current station is an interchange
            is_necessary_interchange = (
                self.stations[from_station].is_interchange and current_line != to_line
            )

            # If this isn't the last segment, check the next station
            if i < len(path) - 2:
                next_station = path[i + 2]
                next_line = self.stations[next_station].line_color

                # If we are at an interchange and the next station is on the same line,
                # we should consider it as an interchange if current_line differs from next_line
                if current_line != to_line and to_line == next_line:
                    is_necessary_interchange = True
                    current_line = to_line

            interchange_message = ""
            if is_necessary_interchange:
                # Determine the platform number based on surrounding stations
                if i > 0:  # Ensure there's a station before the current interchange
                    prev_line = self.stations[path[i - 1]].line_color
                    if self.stations[path[i]].line_color == "black":  # Current station is interchange
                        # Only look at previous and next lines for mapping
                        platform_number = PLATFORM_MAPPING.get((prev_line, to_line))
                        if platform_number is not None:
                            interchange_message = f"Switch to platform no. {platform_number}"
                        else:
                            interchange_message = "Switch platforms (details unavailable)"  # Handle undefined mappings

            journey_details.append({
                'from': from_station,
                'to': to_station,
                'distance': segment.distance,
                'time': segment.time,
                'from_line': from_line,
                'to_line': to_line,
                'is_interchange': is_necessary_interchange,
                'interchange_message': interchange_message
            })

            total_distance += segment.distance
            total_time += segment.time

        # Group journey into segments between required interchanges
        journey_segments = []
        current_segment = {
            'stations': [],
            'distance': 0,
            'time': 0,
            'line_color': current_line
        }

        for detail in journey_details:
            current_segment['stations'].append(detail['from'])
            current_segment['distance'] += detail['distance']
            current_segment['time'] += detail['time']

            if detail['is_interchange']:
                # Complete this segment
                journey_segments.append(current_segment)
                # Add interchange message to the segment
                journey_segments[-1]['interchange_message'] = detail['interchange_message']
                # Start new segment with the new line color
                current_segment = {
                    'stations': [detail['from']],
                    'distance': 0,
                    'time': 0,
                    'line_color': detail['to_line']
                }

        # Add the last segment
        if current_segment['stations']:
            current_segment['stations'].append(journey_details[-1]['to'])
            journey_segments.append(current_segment)

        return {
            'journey_segments': journey_segments,
            'journey_details': journey_details,
            'total_distance': total_distance,
            'total_time': total_time,
            'path': path,
            'num_interchanges': sum(
                1 for detail in journey_details if detail['is_interchange']
            ),
            'interchange_stations': [
                detail['from'] for detail in journey_details
                if detail['is_interchange']
            ]
        }

    def visualize_linear_path(self, path):
        '''     """Generates an image of the path in a straight line from top to bottom."""
        # Create a blank image
        img_width = 200
        img_height = 100 * len(path)
        image = Image.new('RGB', (img_width, img_height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Load a font
        font = ImageFont.load_default()

        # Draw each station on the path
        for idx, station in enumerate(path):
            y = idx * 100 + 50  # Calculate the y position
            # Draw the line connecting the stations
            if idx < len(path) - 1:
                draw.line([(img_width // 2, y), (img_width // 2, y + 100)], fill="black", width=3)
            # Draw the station node
            draw.ellipse([(img_width // 2 - 10, y - 10), (img_width // 2 + 10, y + 10)], fill="red")
            # Draw the station name
            draw.text((img_width // 2 + 20, y - 10), station, font=font, fill="black")

        # Ensure the directory exists
        directory = 'static/metro/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the image with a generic filename
        image_path = os.path.join(directory, 'linear_path_visualization.png')
        image.save(image_path)

        return image_path
        '''        
        return path  

    def format_journey(self, journey_details):
        """Format journey details into a user-friendly string"""
        output = []

        for i, segment in enumerate(journey_details['journey_segments']):
            start = segment['stations'][0]
            end = segment['stations'][-1]
            line_color = segment['line_color']

            output.append(f"{start} → {end} ({line_color} Line)")
            output.append(f"**Duration:** {segment['time']} mins **Distance:** {segment['distance']} m\n")

            # Add interchange instruction if this isn't the last segment
            if segment.get('interchange_message'):
                output.append(f"🚉 {segment['interchange_message']}\n")

            if i < len(journey_details['journey_segments']) - 1:
                next_segment = journey_details['journey_segments'][i + 1]
                output.append(f"⚡ Change from {line_color} Line to {next_segment['line_color']} Line here\n")

        return "\n".join(output)

    def find_path(self, source, destination, mode='time'):
        if source not in self.stations or destination not in self.stations:
            return None, "Invalid station names."

        distances, paths = self._dijkstra(source, destination, mode)

        if destination not in distances:
            return None, "No path found."

        path = self._reconstruct_path(paths, source, destination)
        journey_details = self._get_journey_details(path, mode)

        response = {
            'formatted_journey': self.format_journey(journey_details),
            'path': journey_details['path'],
            'journey_details': journey_details['journey_details'],
            'total_distance': journey_details['total_distance'],
            'total_time': journey_details['total_time'],  # Ensure this key exists
            'interchange_stations': journey_details['interchange_stations']
        }

        return response, None  # Return the response and no error


        return response, None
    def log_station_details(self):
        print("Station Details:\n")
        for station_name, station in self.stations.items():
            interchange_status = "Interchange" if station.is_interchange else "Not an Interchange"
            print(f"Station: {station_name}, Line Color: {station.line_color}, {interchange_status}")

            # Optionally log connections to adjacent stations
            if station_name in self.metro_map:
                connections = [seg.station for seg in self.metro_map[station_name]]
                print(f"  Connected to: {', '.join(connections)}")

        print("\nEnd of Station Details\n")

    def _dijkstra(self, source, destination, mode):
        distances = {source: 0}
        paths = {source: None}
        queue = [(0, source)]

        while queue:
            current_cost, current_station = heapq.heappop(queue)

            if current_station == destination:
                break

            if current_cost > distances[current_station]:
                continue

            for segment in self.metro_map[current_station]:
                cost = current_cost + getattr(segment, mode)

                if segment.station not in distances or cost < distances[segment.station]:
                    distances[segment.station] = cost
                    paths[segment.station] = current_station
                    heapq.heappush(queue, (cost, segment.station))

        return distances, paths

    def _reconstruct_path(self, paths, source, destination):
        path = []
        current = destination

        while current is not None:
            path.append(current)
            current = paths.get(current)

        return list(reversed(path))


    def get_node_positions(self):
        # Define positions for nodes to create a C-shaped metro line representation
        return {
            # Northwest section (ascending)
            'Aluva': (0, 20),
            'Pulinchodu': (2, 18),
            'Companypady': (4, 16),
            'Ambattukavu': (6, 14),
            'Muttom': (8, 12),
            'Kalamassery': (10, 10),

            # Curve towards the city center
            'Cochin University (CUSAT)': (12, 8),
            'Pathadipalam': (14, 6),
            'Edappally': (16, 4),
            'Changampuzha Park': (18, 2),
            'Palarivattom': (20, 0),

            # City center section
            'JLN Stadium': (22, -2),
            'Kaloor': (24, -4),
            'Lissie': (26, -6),
            'Town Hall': (28, -8),
            'M.G. Road': (30, -10),
            "Maharaja's College": (32, -12),

            # Southern section
            'Ernakulam South (Shanthi Nagar)': (34, -14),
            'Kadavanthra': (36, -16),
            'Elamkulam': (38, -18),
            'Vyttila': (40, -20),
            'Thaikoodam': (42, -22),

            # Southeastern curve
            'Petta': (44, -24),
            'Vadakkekotta': (46, -26),
            'SN Junction': (48, -28),
            'Tripunithura Terminal': (50, -30)
        }
    def visualize_metro_map(self, source, destination, current_mode):
        try:
            G = nx.Graph()

            # Define node colors based on metro lines
            line_colors = {
                'blue': {'Aluva', 'Pulinchodu', 'Companypady', 'Ambattukavu', 'Muttom', 'Kalamassery',
                         'Cochin University', 'Pathadipalam', 'Edapally', 'Changampuzha Park', 'Palarivattom',
                         'JLN Stadium', 'Kaloor', 'Lissie', 'MG Road', "Maharaja’s College", 'Ernakulam South',
                         'Kadavanthra', 'Elamkulam', 'Vyttila', 'Thaikoodam', 'Pettah', 'SN Junction', 'Tripunithura'},
                'interchange': {'Aluva', 'Edapally', 'MG Road', 'Vyttila'}  # If any future lines exist
            }

            # Add edges to the graph and set node colors
            for station, neighbors in self.metro_map.items():
                for neighbor in neighbors:
                    weight = neighbor.distance if current_mode == 'distance' else neighbor.time
                    G.add_edge(station, neighbor.station, weight=weight, distance=neighbor.distance, time=neighbor.time)

            # Get node positions
            pos = self.get_node_positions()  # Assume this function is defined elsewhere

            # Ensure all nodes have positions; assign default if missing
            for node in G.nodes():
                if node not in pos:
                    print(f"Node '{node}' has no position, assigning default position.")
                    pos[node] = (0, 0)  # Assign a default position

            # Find path from source to destination first
            path_details, error_message = self.find_path(source, destination, mode=current_mode)
            path_nodes = set(path_details['path']) if path_details else set()

            # Draw nodes with colors based on their respective metro lines
            node_colors = []
            for node in G.nodes():
                if node in path_nodes:
                    # Color nodes in the path black
                    color = 'black'
                else:
                    color = 'lightgray'  # Default color
                    for line, stations in line_colors.items():
                        if node in stations:
                            color = line  # Assign the line color
                            break
                node_colors.append(color)

            # Draw all nodes
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=50, edgecolors='black')

            # Create a path edge list to highlight
            path_edges = []
            if path_details:
                path_nodes = path_details['path']  # List of nodes in the path
                path_edges = [(path_nodes[i], path_nodes[i + 1]) for i in range(len(path_nodes) - 1)]

            # Draw all edges
            nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='gray', width=1.5)

            # Draw the highlighted path edges
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='orange', width=3)

            # Draw arrows on the edges of the path
            for start, end in path_edges:
                start_pos = pos[start]
                end_pos = pos[end]
                arrow = mpatches.FancyArrowPatch(start_pos, end_pos, arrowstyle='->', mutation_scale=10, color='orange', linewidth=2)
                plt.gca().add_patch(arrow)

            # Adjust label positions to the right of the nodes
            labels = {node: node for node in G.nodes()}
            label_pos = {node: (x + 0.1, y) for node, (x, y) in pos.items()}  # Shift labels to the right
            nx.draw_networkx_labels(G, label_pos, labels, font_size=6, verticalalignment='center')

            # Create legend text using journey details
            if path_details:
                total_distance = path_details['total_distance']
                total_time = path_details['total_time']
                legend_text = f'Total Distance: {total_distance} m\nTotal Time: {total_time} min'
            else:
                legend_text = error_message if error_message else 'No journey details available.'

            plt.text(0.95, 0.95, legend_text, transform=plt.gca().transAxes, fontsize=10,
                     verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.8))

            plt.title('Metro Map Visualization')
            plt.axis('off')

            # Ensure the images directory exists
            images_dir = os.path.join('static', 'images')
            os.makedirs(images_dir, exist_ok=True)  # Create the directory if it doesn't exist

            # Save the visualization to a file
            visualization_path = os.path.join(images_dir, 'metro_map_visualization.png')
            plt.savefig(visualization_path, bbox_inches='tight', dpi=150)
            plt.close()

            return visualization_path  # Return the path to the saved image

        except Exception as e:
            import traceback
            traceback.print_exc()  # Print full stack trace for debugging
            return None  # Return None in case of an error


    def get_previous_interchange_station(self, path):
        """Identify previous stations for each interchange in the path."""
        interchange_stops = []

        for i in range(len(path) - 1):
            current_station = self.stations[path[i]]
            next_station = self.stations[path[i + 1]]

            if next_station.is_interchange:  # Check if next station is an interchange
                interchange_stops.append({
                    'station_before_interchange': current_station.name,
                    'interchange_station': next_station.name
                })

        return interchange_stops
