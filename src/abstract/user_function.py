from abc import ABC, abstractmethod
import configparser
import os


class UserFunction(ABC):
    encoding: str = "utf-8"
    jwt_algorithm = "HS256"

    def __init__(self):
        config = configparser.ConfigParser()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, '..', 'env.ini')

        config.read(config_path)

        self.secret_key = config.get('secret_key', 'SECRET_KEY')

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

    # Implement any other methods that should be shared/required by all subclasses.
