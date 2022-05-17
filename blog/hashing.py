from passlib.context import CryptContext

# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def encrypt(password: str):
        return pwd_context.hash(password)

    def verify(plain_password, hashed_password):
        return pwd_context.verify(plain_password,hashed_password)
