import argparse
import logging
from time import sleep

from kafka import KafkaClient
from kafka.errors import NoBrokersAvailable

DEFAULT_MAX_ATTEMPTS = 20
DEFAULT_WAIT_INTERVAL = 1
DEFAULT_KAFKA_SERVER = "kafka:9092"

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

exc = (NoBrokersAvailable,)


def wait_for_kafka(interval: int, attempts: int, host: str) -> None:
    counter = 0

    while counter < attempts:   # noqa: WPS327
        try:    # noqa: WPS229
            counter += 1
            client = KafkaClient(
                bootstrap_servers=host,
                client_id="test",
            )
            if client.bootstrap_connected():
                logger.info("SUCCESS! Connected to Kafka in %d attempts." % counter)
                return
        except exc:
            logger.info(
                "[ATTEMPT %d] Waiting for Kafka to become awailable..." % counter
            )
            sleep(interval)
            continue

    logger.error("Failed to establish connection to Kafka.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View events generator")
    parser.add_argument(
        "--interval",
        default=DEFAULT_WAIT_INTERVAL,
        type=int,
        help="Interval between attempts in seconds, default is 1",
    )
    parser.add_argument(
        "--attempts",
        default=DEFAULT_MAX_ATTEMPTS,
        type=int,
        help="Attempts amount to try, default is 20",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_KAFKA_SERVER,
        help="Kafka server to connect to, default is 'kafka:9092'",
    )
    args = parser.parse_args()
    wait_for_kafka(args.interval, args.attempts, args.host)
