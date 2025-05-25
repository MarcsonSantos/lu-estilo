from jose.exceptions import JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.crud.users import get_user_by_email
from app.db.models.users import User
from app.db.session import get_db

# Dependência que extrai e valida o usuário autenticado a partir do token JWT
# Utilizada em rotas protegidas para garantir que apenas usuários autenticados tenham acesso

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Define a URL de login usada para obter o token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Decodifica o token JWT e retorna o usuário correspondente.

    - Extrai o token do header Authorization: Bearer <token>
    - Valida o token usando a função decode_token
    - Recupera o e-mail do payload do token (campo 'sub')
    - Busca o usuário no banco de dados
    - Retorna o objeto User se válido, ou lança HTTP 401 em caso de erro
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica o token JWT para extrair os dados
        payload = decode_token(token)
        email = payload.get("sub")  # O e-mail do usuário é armazenado no campo 'sub' do token
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Busca o usuário pelo e-mail extraído do token
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user  # Retorna o usuário autenticado