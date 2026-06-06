# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up --build -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Restart a specific service
docker-compose restart backend

# Rebuild without cache
docker-compose build --no-cache