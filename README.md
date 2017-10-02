## Start
`docker-compose build
docker-compose up -d`

docker-compose.yml contains mongo image for ARM (raspberry pi), to start it on normal kerner replace image with mongo:latest

Also don't forget to rename example.env to .env and add your data there

## Import data
`docker compose exec bot python3 ../load_data.py`