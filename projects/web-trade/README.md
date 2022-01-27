# Up docker-compose
docker-compose up

# Verify containers
docker ps -a

# Update changes in docker-compose and clean
docker-compose up --force-recreate --build -d
docker image prune -f