import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.settings import settings

# Contexto do PassLib para gerar e verificar senhas com o algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Gera um hash seguro a partir de uma senha em texto.

    Args:
        password (str): Senha em texto.

    Returns:
        str: Hash da senha.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Args:
        plain_password (str): Senha fornecida pelo usuário.
        hashed_password (str): Hash armazenado da senha.

    Returns:
        bool: True se a senha for válida, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=1000)) -> str:
    """
    Cria um token JWT com as informações fornecidas e tempo de expiração.

    Args:
        data (dict): Dados a serem codificados no token (ex: email).
        expires_delta (timedelta, optional): Tempo de expiração do token.

    Returns:
        str: Token JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str):
    """
    Decodifica um token JWT e retorna os dados contidos nele.

    Args:
        token (str): Token JWT codificado.

    Returns:
        dict: Dados decodificados do token.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
