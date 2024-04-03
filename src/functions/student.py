import bcrypt
from datetime import datetime, timedelta
from jose import jwt

from abstract.user_function import UserFunction


class StudentFunction(UserFunction):

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
        if id == 'admin':
            role = "admin"
        else:
            role = "student"
        return jwt.encode(
            {
                "sub": id,
                "exp": datetime.now() + timedelta(days=1),
                "role": role
            },
            self.secret_key,
            algorithm=self.jwt_algorithm
        )

    def decode_jwt(self, access_token: str):
        payload: dict = jwt.decode(
            access_token, self.secret_key, algorithms=[self.jwt_algorithm]
        )

        return payload
