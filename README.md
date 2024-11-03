# Metro Navigation

Metro Navigation is a web application designed to provide users with information about metro routes, schedules, and navigation assistance. This project utilizes Django for the backend and is containerized using Docker to ensure a consistent development and deployment environment.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Building the Docker Image](#building-the-docker-image)
- [Publishing to Docker Hub](#publishing-to-docker-hub)
- [Pulling and Running the Application](#pulling-and-running-the-application)
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
- Docker Compose (optional, for multi-container setups).

### Cloning the Repository
```
git clone https://github.com/deekshith0509/MetroNavigator-WebApp.git
cd MetroNavigator-WebApp
```

## Building the Docker Image
1. **Build the Docker image** using the Dockerfile in the repository:
```
docker build -t deekshith7878/metro_navigation:v2.0 .
```

## Publishing to Docker Hub
1. **Log in to Docker Hub:**
```
docker login
```

2. **Push the Docker image** to your Docker Hub repository:
```
docker push deekshith7878/metro_navigation:v2.0
```

## Pulling and Running the Application

If you want to run the application without building it again, you can pull the existing image directly from Docker Hub.

1. **Pull the Docker image:**
```
docker pull deekshith7878/metro_navigation:v2.0
```

2. **Run the Docker container using the existing image:**
```
docker run -d -p 8000:8000 deekshith7878/metro_navigation:v2.0
```

3. **Access the application:** Open your browser and go to https://<your-server-ip>:8000.


## Manual Execution (Without Docker)

1. **Install the required dependencies**. Make sure you have requirements.txt in your project directory, and install the requirements using:
```
pip install -r requirements.txt
```

 2.**Create SSL certificates** (if not already created): 
If you don't have *cert.pem* and *key.pem*, you can generate them with OpenSSL:
```
mkdir certs
openssl req -x509 -newkey rsa:4096 -nodes -out certs/cert.pem -keyout certs/key.pem -days 365 -subj '/CN=*'
```

3. **Run the application** using runserver_plus:
```
python manage.py runserver_plus 0.0.0.0:8000 --cert-file certs/cert.pem --key-file certs/key.pem
```

4. **Access the application:** Open your browser and go to https://localhost:8000.




## Why Docker?

**Consistency :** Docker ensures that your application runs in the same environment across different machines, eliminating the "it works on my machine" problem.

**Isolation :** Docker containers provide an isolated environment for your application, ensuring that it doesn't interfere with other applications running on the same machine.

**Portability :** Docker images can be easily shared and deployed across different environments, from local development machines to cloud servers.

**Efficiency :** Docker images are lightweight and can be started quickly, improving development and deployment efficiency.
## Usage
 - To run the application using Docker, follow the steps under Pulling and Running the Application.
 - To run the application manually, follow the steps under Manual Execution (Without Docker).
 - Ensure you have your SSL certificates in the certs directory.

## Contributing

Contributions are welcome! Please create a pull request for any improvements or bug fixes.
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
