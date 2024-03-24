import bcrypt


class StudentFunction:
    encoding: str = "utf-8"

    def encrypt_pw(self, plain_pw: str) -> str:
        encrypted_pw: bytes = bcrypt.hashpw(
            plain_pw.pw.encode(self.encoding),
            salt=bcrypt.gensalt()
        )

        return encrypted_pw.decode(self.encoding)
