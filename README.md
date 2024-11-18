# mindinventory-api
API to Analyze User Intent and Generate Personalized Emails based on Website Interaction

## Features
- Creation and storage of case studies in Neo4j
- Intent detection and user interest identification
- Matching projects using similarity search with Neo4j
- Personalized email generation
- FastAPI integration for API endpoints
- Dockerized application for easy deployment

## Prerequisites
- **Docker** installed on your machine
- **Python 3.9** or higher for local testing

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mindinventory-api.git
   cd mindinventory-api

2. **Build the Docker image:**
   ```bash
   docker build -t mindinventory-api:python3.9 .

3. **Run the Docker container:**
   ```bash
   docker run -d -p 8000:8000 --name mindinventory-api mindinventory-api:python3.9

4. **Access the API:**
   Already added postman collection. 


