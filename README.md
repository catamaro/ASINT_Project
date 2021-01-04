# ASINT_Project

Requirements: 
    - $pip install requirements.txt

To run project:
    - $chmod +x open_apps.sh
    - $./open_apps.sh

Microservices:
    - Videos
    - QA
    - User Manager
    - Logs
    - Stats

Proxy Funcionalities:
    - Add new microservices without changing the proxy code
        - requires a port number where the microservice is running
        - requires a name that must be the same from the API endpoint
          e.g name=videos -> endpoint="API/videos/remaining_path"
        - the microservices implemented are already registeres in the 
          proxy db
    - Add new pages without changing the proxy code
        - html page must have the same name has the endpoint
          e.g name=videos.html -> endpoint="/videos"
    - Login via fenix 
    - Logs and Stats fowarding 