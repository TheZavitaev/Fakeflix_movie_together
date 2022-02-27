import logging
from abc import ABC, abstractmethod
from functools import lru_cache

from core.config import settings
from db.kafka import AbstractKafkaProducer, get_kafka_producer
from fastapi import Depends
from models.models import ViewedFrame


class AbstractMovieProgressService(ABC):
    @abstractmethod
    async def add(self, event: ViewedFrame):
        pass


class MovieProgressService(AbstractMovieProgressService):
    def __init__(self, kafka_producer: AbstractKafkaProducer):
        self.kafka_producer = kafka_producer

    async def add(self, event: ViewedFrame):
        logging.info(f'user_id {event.user_id}, movie_id {event.movie_id}, movie_timestamp {event.movie_timestamp}')
        key = f'{event.user_id}+{event.movie_id}'

        await self.kafka_producer.send(settings.kafka_movie_progress_topic, key, event.json())


@lru_cache()
def get_movie_progress_service(
        kafka_producer: AbstractKafkaProducer = Depends(get_kafka_producer),
) -> AbstractMovieProgressService:
    return MovieProgressService(kafka_producer)
