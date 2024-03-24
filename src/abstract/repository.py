from fastapi import Depends
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic

from database.database import get_database

T = TypeVar('T')

class Repository(ABC, Generic[T]):


    def __init__(self, session: Session = Depends(get_database)):
        self.session = session

    
    @abstractmethod
    def get_all_entities(self) -> List[T]:
        pass

    
    @abstractmethod
    def get_entity_by_id(self, id) -> T | None:
        pass


    @abstractmethod
    def create_entity(self, entity: T) -> T:
        pass


    @abstractmethod
    def update_entity_by_id(self, id, request) -> T:
        pass


    @abstractmethod
    def delete_entity_by_id(self, id) -> T:
        pass