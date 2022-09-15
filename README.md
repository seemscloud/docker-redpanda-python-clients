```bash
docker build . --tag theanotherwise/kafka-end-to-end-latency:latest

docker push theanotherwise/kafka-end-to-end-latency:latest

docker-compose up --build --remove-orphans --force-recreate
```