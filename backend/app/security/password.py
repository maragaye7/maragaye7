import bcrypt

# bcrypt tronque silencieusement au-dela de 72 octets : on le documente et
# on refuse explicitement un mot de passe trop long plutot que de le
# tronquer silencieusement.
_MAX_PASSWORD_BYTES = 72


def hash_password(plain_password: str) -> str:
    encoded = plain_password.encode("utf-8")
    if len(encoded) > _MAX_PASSWORD_BYTES:
        raise ValueError("Mot de passe trop long (72 octets maximum).")
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
