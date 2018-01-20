from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["sha512_crypt", "des_crypt"],

    deprecated="auto"
    )
