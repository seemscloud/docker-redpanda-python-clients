rpk topic create filebeat \
  --replicas 1 \
  --partitions 8 \
  --topic-config segment.bytes=536870912 \
  --topic-config retention.ms=3600000 \
  --topic-config retention.bytes=-1 