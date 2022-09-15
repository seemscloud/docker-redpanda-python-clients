```bash
docker build . --tag theanotherwise/kafka-end-to-end-latency:latest

docker push theanotherwise/kafka-end-to-end-latency:latest
```

```bash
docker-compose up --build --remove-orphans --force-recreate
```

```bash
avg(rate(kafka_end_to_end_latency[4s]))
```