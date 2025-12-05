from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# =========================
# MODELOS
# =========================
class Comando(BaseModel):
    accion: str

class Estado(BaseModel):
    temp: float | None = None
    hum: float | None = None
    puerta: str | None = None
    garage: str | None = None
    luces: str | None = None


# =========================
# VARIABLES GLOBALES
# =========================
ultimo_comando = {"accion": "ninguno"}

estado_esp32 = {
    "temp": None,
    "hum": None,
    "puerta": None,
    "garage": None,
    "luces": None
}


# =========================
# RUTAS PRINCIPALES
# =========================

@app.get("/")
def home():
    return {"mensaje": "Backend IoT funcionando correctamente"}

# ----- APP ENVÍA COMANDO -----
@app.post("/comando")
def recibir_comando(cmd: Comando):
    global ultimo_comando
    ultimo_comando = cmd.dict()
    return {"status": "ok", "comando_recibido": ultimo_comando}

# ----- ESP32 PIDE EL ÚLTIMO COMANDO -----
@app.get("/comando")
def enviar_comando():
    global ultimo_comando
    cmd = ultimo_comando.copy()
    # limpiar el comando para evitar repetirlo
    ultimo_comando = {"accion": "ninguno"}
    return cmd

# ----- ESP32 ENVÍA SU ESTADO -----
@app.post("/estado")
def recibir_estado(data: Estado):
    global estado_esp32
    estado_esp32 = data.dict()
    return {"status": "ok"}

# ----- APP PIDE EL ESTADO DEL ESP32 -----
@app.get("/estado")
def obtener_estado():
    return estado_esp32
