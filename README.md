# getJobBot
This bot will have a conversation with you on various topics, support You, charge you with motivation and give advice!

# Docker image of bot
Build the docker image using:
```
cd .\src\app
docker build . -t bot 
```
Generate the docker container on port 8000 using:
```
docker run --name bot main
```

# Docker compose of ClickHouse
Run docker compose file with ClickHouse on port 8123
```
cd ../..
docker-compose up
```
