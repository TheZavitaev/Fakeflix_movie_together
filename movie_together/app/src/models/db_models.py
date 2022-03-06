import uuid

from sqlalchemy import Column, String, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Room(Base):
    __tablename__ = 'movie_together_room'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    film_work_uuid = Column(UUID(as_uuid=True))
    link = Column(String)
    status = Column(String)

    owner_uuid = Column(UUID, nullable=False, unique=True)
    room_users = relationship('RoomUser')

    created_at = Column(DateTime, server_default=func.now())


class RoomUser(Base):
    __tablename__ = 'movie_together_room_user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_uuid = Column(UUID(as_uuid=True))
    room_uuid = Column(ForeignKey('movie_together_room.id'))
    user_type = Column(String)

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (UniqueConstraint('user_uuid', 'room_uuid', name='unique_room_user'), )