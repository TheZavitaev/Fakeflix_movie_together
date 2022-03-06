import logging
import random
import typing
import uuid
from abc import ABC, abstractmethod
from time import sleep

import models
import urls
from config import settings
from faker import Faker
from limited_list import LimitedList

import utils

logger = logging.getLogger("ugc")

REVIEWS_MAX_LENGTH = 100


class BaseGenerator(ABC):
    @abstractmethod
    def __init__(self, max_batch: int):
        ...  # noqa: WPS428

    @abstractmethod
    def generate(self) -> typing.Generator:
        ...  # noqa: WPS428


class ContentGenerator(BaseGenerator):
    def __init__(self, max_batch: int = 5):
        super(ContentGenerator, self).__init__(max_batch)  # noqa: WPS608
        self.max_batch = max_batch
        self.fake = Faker()
        self.film_pool = [models.Film() for _ in range(self.max_batch)]
        self.user_pool = [models.User() for _ in range(self.max_batch)]
        self.review_pool = LimitedList(REVIEWS_MAX_LENGTH)

    def generate(self) -> typing.Generator:

        while True:  # noqa: WPS457
            yield self._generate_reviews(
                random.randint(1, self.max_batch)
            ) + self._generate_film_likes(
                random.randint(1, self.max_batch)
            ) + self._generate_review_likes(
                random.randint(1, self.max_batch)
            ) + self._generate_bookmarks(
                random.randint(1, self.max_batch)
            )
            sleep(settings.BATCH_INTERVAL)
            logger.info("content batch sent")

    def _generate_reviews(self, batch_size: int) -> list[tuple[str, dict]]:
        reviews = []
        for _ in range(batch_size):
            review = models.Review(
                movie_id=random.choice(self.film_pool).movie_id,
                user_id=random.choice(self.user_pool).user_id,
                user_rating=random.choice(utils.ReviewRate.choices()),
                text=self.fake.text(),
            )
            reviews.append((urls.DataType.REVIEW.value, review.dict()))
            self.review_pool.append(review)
        return reviews

    def _generate_film_likes(self, batch_size: int) -> list[tuple[str, dict]]:
        return [
            (
                urls.DataType.FILM_LIKE.value,
                models.FilmLike(
                    movie_id=random.choice(self.film_pool).movie_id,
                    user_id=random.choice(self.user_pool).user_id,
                    rating=random.choice(utils.LikeRate.choices()),
                ).dict(),
            )
            for _ in range(batch_size)
        ]

    def _generate_review_likes(self, batch_size: int) -> list[tuple[str, dict]]:
        return [
            (
                urls.DataType.REVIEW_LIKE.value,
                models.ReviewLike(
                    review_id=random.choice(self.review_pool.values()).review_id,
                    user_id=random.choice(self.user_pool).user_id,
                    rating=random.choice(utils.LikeRate.choices()),
                ).dict(),
            )
            for _ in range(batch_size)
        ]

    def _generate_bookmarks(self, batch_size: int) -> list[tuple[str, dict]]:
        return [
            (
                urls.DataType.BOOKMARK.value,
                models.Bookmark(
                    bid=str(uuid.uuid4()),
                    user_id=random.choice(self.user_pool).user_id,
                    movie_id=random.choice(self.film_pool).movie_id,
                ).dict(),
            )
            for _ in range(batch_size)
        ]


class ViewsGenerator(BaseGenerator):
    def __init__(self, max_batch: int):
        super(ViewsGenerator, self).__init__(max_batch)  # noqa: WPS608
        self.max_batch = max_batch
        self.film_pool = [models.Film() for _ in range(self.max_batch)]
        self.user_pool = [models.User() for _ in range(self.max_batch)]

    def generate(self) -> typing.Generator:

        while True:  # noqa: WPS457
            yield self._generate_batch(random.randint(1, self.max_batch))
            sleep(settings.BATCH_INTERVAL)
            logger.info("film views batch sent")

    def _generate_batch(self, batch_size: int) -> list[tuple[str, dict]]:
        batch = []
        for _ in range(batch_size):
            batch.append(
                (
                    urls.DataType.VIEW.value,
                    models.FilmView(
                        movie_id=random.choice(self.film_pool).movie_id,
                        user_id=random.choice(self.user_pool).user_id,
                        movie_timestamp=random.randint(
                            settings.FILM_MIN_LENGTH, settings.FILM_MAX_LENGTH
                        ),
                    ).dict(),
                )
            )
        return batch
