# Metro Navigation


<p align="center">
  <img src="images/main.jpg" alt="Metro Navigator Main Screen" width="200">
  <img src="images/main2.jpg" alt="Metro Navigator Alternate View" width="200">
  <img src="images/pop.jpg" alt="Metro Navigator Popup" width="200">
</p>

<p align="center">
  <img src="images/ui1.jpg" alt="Metro Navigator UI 1" width="200">
  <img src="images/ui2.jpg" alt="Metro Navigator UI 2" width="200">
  <img src="images/ui3.jpg" alt="Metro Navigator UI 3" width="200">
</p>



MetroNavigator-WebApp is a Django-based application designed for metro route visualization and journey planning. It employs Dijkstra's algorithm to find optimal paths. The project highlights full-stack development with Python and Django, emphasizing algorithmic applications and real-time navigation. Users can locate the nearest metro station and receive comprehensive journey summaries, including interchanges, expected departure times, and travel distances.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Manual Execution (Without Docker)](#manual-execution-without-docker)
- [Why Docker?](#why-docker)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features
- Provides real-time information about metro routes and schedules.
- User-friendly interface built with Material Design principles.
- HTTPS support using self-signed SSL certificates.
- Responsive design for optimal use on various devices.

## Technologies Used
- Django
- Docker
- Python
- Matplotlib
- NetworkX
- OpenSSL (for SSL certificate generation)

## Getting Started

### Prerequisites
- Python 3.x installed on your machine (for manual execution).
- Docker installed on your machine (for Docker execution).
- Docker Compose (for multi-container setups).

### Cloning the Repository
```
git clone https://github.com/deekshith0509/MetroNavigator-WebApp.git
cd MetroNavigator-WebApp
```

## Running the Application

1. **Ensure Docker is installed and running.**
2. **Start the application using Docker Compose:**
```
docker-compose up -d
```
3. **Access the application:** Open your browser and go to `https://<your-server-ip>:8000`.


## Why Docker?

>**Consistency:** Docker ensures that your application runs in the same environment across different machines, eliminating the "it works on my machine" problem.

>**Isolation:** Docker containers provide an isolated environment for your application, ensuring that it doesn't interfere with other applications running on the same machine.

>**Portability:** Docker images can be easily shared and deployed across different environments, from local development machines to cloud servers.

>**Efficiency:** Docker images are lightweight and can be started quickly, improving development and deployment efficiency.

## Usage
 - To run the application using Docker, follow the steps under **Running the Application**.
 - To run the application manually, follow the steps under **Manual Execution (Without Docker)**.
 - Ensure you have your SSL certificates in the `certs` directory.

## Contributing

Contributions are welcome! Please create a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

