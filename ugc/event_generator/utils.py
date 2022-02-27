import logging
from enum import Enum

logger = logging.getLogger("ugc")


class Rating(Enum):

    @classmethod
    def choices(cls):
        return [choice.value for choice in cls]


class LikeRate(Rating):
    LIKE = "LIKE"
    DISLIKE = "DISLIKE"


class ReviewRate(Rating):
    LIKE = 1
    DISLIKE = 0


def backoff_hdlr(details: dict) -> None:
    logger.info(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function '{target.__name__}'".format(**details)  # noqa: C812, WPS326
    )
