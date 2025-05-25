import time
from sqlalchemy.exc import OperationalError
from app.db.session import engine
from app.db.base import Base

def init_db(max_retries: int = 10, delay: int = 2):
    for attempt in range(max_retries):
        try:
            print(f"Tentando conectar ao banco... Tentativa {attempt + 1}")
            Base.metadata.create_all(bind=engine)
            print("Tabelas criadas com sucesso.")
            return
        except OperationalError as e:
            print(f"Banco ainda não está pronto: {e}")
            time.sleep(delay)
    print("Falha ao conectar ao banco após várias tentativas.")
