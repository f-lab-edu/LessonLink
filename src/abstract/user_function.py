from abc import ABC, abstractmethod
from functions.init_file import get_init_config_data


class UserFunction(ABC):
    encoding: str = "utf-8"
    jwt_algorithm = "HS256"

    def __init__(self):
        self.secret_key = get_init_config_data('secret_key', 'SECRET_KEY')

    @abstractmethod
    def encrypt_pw(self, plain_pw: str) -> str:
        pass

    @abstractmethod
    def verify_pw(self, plain_pw, hashed_pw) -> bool:
        pass

    @abstractmethod
    def create_jwt(self, id: str) -> str:
        pass

    @abstractmethod
    def decode_jwt(self, access_token: str) -> str:
        pass
