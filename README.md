```bash
docker build . --tag theanotherwise/kafka-end-to-end-latency:1.0.0

docker push theanotherwise/kafka-end-to-end-latency:1.0.0
```

```bash
docker-compose up --build --remove-orphans --force-recreate
```

```bash
avg(rate(kafka_end_to_end_latency[4s]))
```