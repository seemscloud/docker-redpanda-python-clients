import os
import json
import time
import logging
import string
import random
import statistics

from scipy import stats
from kafka import KafkaProducer, KafkaConsumer
from multiprocessing import Process, Queue
from threading import Thread
from prometheus_client import start_http_server, Counter, Gauge, multiprocess, CollectorRegistry

LOGLEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)

kafka_end_to_end_avg_latency = Gauge('kafka_end_to_end_avg_latency', 'Kafka end to end latency')
kafka_end_to_end_perc_latency = Gauge('kafka_end_to_end_perc_latency', 'Kafka end to end latency')


def compose_headers():
    return [("timestamp", timestamp_ms().encode('utf_8'))]


def flush(self):
    self.producer.flush()


def producer_loop(endpoints, topic, message_size, batch_size, linger_ms, compression_type, acks):
    if compression_type == "None":
        compression_type = None

    producer = KafkaProducer(bootstrap_servers=endpoints,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                             linger_ms=linger_ms, batch_size=batch_size, compression_type=compression_type,
                             acks=acks)

    content = random_string(message_size)

    while True:
        headers = compose_headers()

        producer.send(topic, content, headers=headers)
        producer.flush()


def calc_latency(latenciesQueue, percentage_value):
    while True:
        latencies = [0]
        for i in range(latenciesQueue.qsize()):
            latencies.append(latenciesQueue.get())

        kafka_end_to_end_avg_latency.inc(statistics.mean(latencies))
        kafka_end_to_end_perc_latency.inc(stats.percentileofscore(latencies, percentage_value, kind='mean'))

        time.sleep(1)


def consumer_loop(endpoints, topic, group_name, percentage_value):
    consumer = KafkaConsumer(topic, bootstrap_servers=endpoints, enable_auto_commit=False, group_id=group_name,
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))

    latenciesQueue = Queue()

    Process(target=calc_latency, args=(latenciesQueue, percentage_value,)).start()

    for msg in consumer:
        latenciesQueue.put(int(timestamp_ms()) - int(msg.headers[0][1].decode()))


def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))


def to_bytes(data):
    return data.encode("UTF-8")


def timestamp_ms():
    return "{}".format(int(time.time() * 1000))


def parse_servers(data):
    return list(filter(None, data.split(",")))


def calc_delay(delay):
    return int(delay) * 0.001


def main():
    message_size = int(os.environ["MESSAGE_SIZE"])
    topic_name = os.environ["TOPIC_NAME"]
    group_name = os.environ["GROUP_NAME"]

    batch_size = int(os.environ["BATCH_SIZE"])
    linger_ms = int(os.environ["LINGER_MS"])
    compression_type = os.environ["COMPRESSION"]
    acks = os.environ["ACKS"]

    percentage_value = float(os.environ["PERCENTAGE_VALUE"])
    endpoints = parse_servers(os.environ["BOOTSTRAP_SERVERS"])

    Process(target=producer_loop, args=(
        endpoints, topic_name, message_size, batch_size, linger_ms, compression_type, acks)).start()

    Process(target=consumer_loop, args=(endpoints, topic_name, group_name, percentage_value)).start()


if __name__ == "__main__":
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    start_http_server(8000, registry=registry)

    init_delay = calc_delay(os.environ["INIT_DELAY"])
    time.sleep(init_delay)

    main()
