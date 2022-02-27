import argparse
import asyncio
import logging
from logging.config import fileConfig

import generator
import producers  # noqa: F401
from config import settings

fileConfig(settings.LOGGING_CONFIG_FILE)
logger = logging.getLogger("ugc")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View events generator")
    parser.add_argument(
        "datatype", choices=["views", "content"], help="Specify data to generate"
    )
    parser.add_argument(
        "--host",
        default="http://localhost",
        help="UGC API host with schema, http://localhost by default",
    )
    parser.add_argument(
        "--batch", type=int, default=5, help="Maximum batch size, 5 by default"
    )
    args = parser.parse_args()
    asyncio.run(
        generator.run_generator(
            datatype=args.datatype, max_batch_size=args.batch, host=args.host
        )
    )
