from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from database.database_init import get_database, get_async_database

EducationalEntity = TypeVar('EducationalEntity')
Request = TypeVar('Request')
T = TypeVar('T')


class Repository(ABC, Generic[EducationalEntity]):

    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    @abstractmethod
    def get_all_entities(self) -> List[EducationalEntity]:
        pass

    @abstractmethod
    def get_entity_by_id(self, id: T) -> EducationalEntity | None:
        pass

    @abstractmethod
    def create_entity(self, entity: EducationalEntity) -> EducationalEntity:
        pass

    @abstractmethod
    def update_entity_by_id(self, id: T, request: Request) -> EducationalEntity:
        pass

    @abstractmethod
    def delete_entity_by_id(self, id: T) -> EducationalEntity:
        pass


class RepositoryAsync(ABC, Generic[EducationalEntity]):

    def __init__(self, session: AsyncSession = Depends(get_async_database)):
        self.session = session

    @abstractmethod
    async def get_all_entities(self) -> List[EducationalEntity]:
        pass

    @abstractmethod
    async def get_entity_by_id(self, id: T) -> EducationalEntity | None:
        pass

    @abstractmethod
    async def create_entity(self, entity: EducationalEntity) -> EducationalEntity:
        pass

    @abstractmethod
    async def update_entity_by_id(self, id: T, request: Request) -> EducationalEntity:
        pass

    @abstractmethod
    async def delete_entity_by_id(self, id: T) -> EducationalEntity:
        pass