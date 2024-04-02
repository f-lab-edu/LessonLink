from fastapi import Depends
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from database.database import get_database

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
    def update_entity_by_id(self, id: T, request) -> EducationalEntity:
        pass

    @abstractmethod
    def delete_entity_by_id(self, id: T) -> EducationalEntity:
        pass
