# Movie Tracker 🎬

A web app for exploring movies, saving favorites, and getting personalized recommendations.

## Key Features  
- **Search & Save**: Browse movies via TMDB API and create a personal list.  
- **Discover**: Get suggestions based on your saved movies.  
- **Admin Dashboard**: Manage user profiles (create/delete).  

## Tech Stack  
- **Frontend**: Bootstrap + Custom CSS  
- **Backend**: Flask (integrates with TMDB API)  
- **Database**: MySQL  
- **Infra**: Docker Compose (multi-container setup)  
  - `nginx` (HTTPS reverse proxy)  
  - `flask-app` (core logic)  
  - `discover-engine` (recommendation microservice)
  - `movie-db` (MySQL database)

## Run Locally
1. `git clone https://github.com/Luca-Sid/Movie_Tracker.git`
2. Modify `.env_example` with secure credentials and rename it to `.env`
3. Run `generate-ssl.sh` to create a self-signed certificate
4. Run `docker compose up --build -d`