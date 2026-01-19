from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os

from src.database import Database
from src.api_logic import (
    search_player_api,
    get_classification_data,
    get_team_stats,
    update_laliga_data_api
)
from src.email_utils import send_verification_email
from src.validators import validate_email, validate_password, validate_username


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = Database()


class UserLogin(BaseModel):
    username: str
    password: str

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class PlayerSearch(BaseModel):
    name: str

class VerifyCode(BaseModel):
    username: str
    code: str

class ResendCode(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class ForgotPassword(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

class ResetPassword(BaseModel):
    username: str
    code: str
    new_password: str


@app.post("/api/login")
def login(user: UserLogin):
    success, message = db.authenticate(user.username.lower(), user.password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    return {"status": "success", "username": user.username, "message": message}


@app.post("/api/register")
def register(user: UserRegister):
    # Validaciones backend
    is_u, msg_u = validate_username(user.username.lower())
    if not is_u:
        raise HTTPException(status_code=400, detail=msg_u)

    if not validate_email(user.email.lower()):
        raise HTTPException(status_code=400, detail="Formato de email inválido")

    is_p, msg_p = validate_password(user.password)
    if not is_p:
        raise HTTPException(status_code=400, detail=msg_p)

    success, result = db.register_user(
        user.username.lower(),
        user.email.lower(),
        user.password
    )
    if not success:
        raise HTTPException(status_code=400, detail=result)

    verification_code = result
    try:
        send_verification_email(user.email, verification_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo enviar el correo: {str(e)}")

    return {"status": "pending", "message": "Se ha enviado un código de verificación a tu correo"}


@app.post("/api/verify")
def verify_account(data: VerifyCode):
    success, message = db.verify_user(data.username.lower(), data.code)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"status": "success", "message": message}


@app.post("/api/resend-code")
def resend_code(data: ResendCode):
    success, result = db.resend_verification_code(
        username=(data.username.lower() if data.username else None),
        email=(data.email.lower() if data.email else None)
    )
    if not success:
        raise HTTPException(status_code=400, detail=result)

    to_email = result["email"]
    code = result["code"]

    try:
        send_verification_email(to_email, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo reenviar el correo: {str(e)}")

    return {"status": "pending", "message": "Código reenviado. Revisa tu correo."}


@app.post("/api/forgot-password")
def forgot_password(data: ForgotPassword):
    success, result = db.request_password_reset(
        username=(data.username.lower() if data.username else None),
        email=(data.email.lower() if data.email else None)
    )
    if not success:
        raise HTTPException(status_code=400, detail=result)

    to_email = result["email"]
    code = result["code"]

    try:
        # Reutilizamos el email de verificación para enviar el código
        send_verification_email(to_email, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo enviar el correo: {str(e)}")

    return {"status": "pending", "message": "Se envió un código para restablecer la contraseña. Revisa tu correo."}


@app.post("/api/reset-password")
def reset_password(data: ResetPassword):
    is_p, msg_p = validate_password(data.new_password)
    if not is_p:
        raise HTTPException(status_code=400, detail=msg_p)

    success, message = db.reset_password(data.username.lower(), data.code, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"status": "success", "message": message}


# -----------------------------
# LaLiga Routes
# -----------------------------
@app.get("/api/laliga")
def get_laliga_classification():
    data = get_classification_data()
    if isinstance(data, dict) and "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data


@app.post("/api/laliga/update")
def update_laliga():
    result = update_laliga_data_api()
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message", "Error desconocido"))
    return result


@app.get("/api/laliga/{team_name}")
def get_team_detail(team_name: str):
    data = get_team_stats(team_name)
    if not data:
        raise HTTPException(status_code=404, detail="Team not found")
    return data


@app.post("/api/scout")
def scout_player(search: PlayerSearch):
    result = search_player_api(search.name)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result



static_path = os.path.join(os.getcwd(), "frontend_static")
if not os.path.exists(static_path):
    os.makedirs(static_path)

app.mount("/", StaticFiles(directory=static_path, html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading
    import time

    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://localhost:8000")

    print("Iniciando servidor... El navegador se abrirá automáticamente.")
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=8000)

