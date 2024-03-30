import bcrypt
import configparser
import os
from datetime import datetime, timedelta
from jose import jwt


class StudentFunction:
    encoding: str = "utf-8"
    jwt_algorithm = "HS256"

    def __init__(self):
        config = configparser.ConfigParser()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, '..', 'env.ini')

        config.read(config_path)

        self.secret_key = config.get('secret_key', 'SECRET_KEY')

    def encrypt_pw(self, plain_pw: str) -> str:
        encrypted_pw: bytes = bcrypt.hashpw(
            plain_pw.encode(self.encoding),
            salt=bcrypt.gensalt()
        )

        return encrypted_pw.decode(self.encoding)

    def verify_pw(self, plain_pw, hashed_pw):
        return bcrypt.checkpw(
            plain_pw.encode(self.encoding),
            hashed_pw.encode(self.encoding)
        )

    def create_jwt(self, id: str):
        return jwt.encode(
            {
                "sub": id,
                "exp": datetime.now() + timedelta(days=1)
            },
            self.secret_key,
            algorithm=self.jwt_algorithm
        )
