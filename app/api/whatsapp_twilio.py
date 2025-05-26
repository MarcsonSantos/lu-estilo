import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.settings import settings
from app.db.session import get_db
from app.api.auth import get_current_user
from app.db.models.users import User

router = APIRouter(prefix="/twilio", tags=["whatsapp"])


@router.post("/send")
def send_whatsapp_message(
    to: str,
    message: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem enviar mensagens.")

    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"

    data = {
        "From": settings.TWILIO_SANDBOX_NUMBER,
        "To": f"whatsapp:{to}",
        "Body": message
    }

    auth = (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    try:
        response = httpx.post(url, data=data, auth=auth)
        response.raise_for_status()  # lança erro com mensagem completa
    except httpx.HTTPStatusError as e:
        print("Erro HTTP Twilio:", e.response.text)
        raise HTTPException(status_code=500, detail=f"Erro Twilio: {e.response.text}")
    except Exception as e:
        print("Erro geral:", str(e))
        raise HTTPException(status_code=500, detail="Erro inesperado ao enviar mensagem")

    return {"detail": "Mensagem enviada com sucesso", "sid": response.json()["sid"]}
