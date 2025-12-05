from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ============================
# MODELOS
# ============================
class Comando(BaseModel):
    accion: str

class Estado(BaseModel):
    temp: float | None = None
    hum: float | None = None

    puerta: str | None = None
    garage: str | None = None

    cocina: str | None = None
    sala: str | None = None
    dormitorio: str | None = None

    grupoA: str | None = None
    grupoB: str | None = None

    pir: str | None = None
    ultrasonico: str | None = None


# ============================
# VARIABLES GLOBALES
# ============================
ultimo_comando = {"accion": "ninguno"}

estado_esp32 = {
    "temp": 0.0,
    "hum": 0.0,
    
    "puerta": "desconocido",
    "garage": "desconocido",

    "cocina": "off",
    "sala": "off",
    "dormitorio": "off",

    "grupoA": "off",
    "grupoB": "off",

    "pir": "inactivo",
    "ultrasonico": "inactivo"
}

# ============================
#   RUTA PRINCIPAL
# ============================
@app.get("/")
def home():
    return {"mensaje": "Backend IoT funcionando correctamente"}


# ============================
# APP ENVÍA UN COMANDO → GUARDAR
# ============================
@app.post("/comando")
def recibir_comando(cmd: Comando):
    global ultimo_comando
    ultimo_comando = {"accion": cmd.accion}
    return {"status": "ok", "accion_guardada": cmd.accion}


# ============================
# ESP32 PIDE COMANDO → ENTREGAR Y BORRAR
# ============================
@app.get("/comando")
def enviar_comando():
    global ultimo_comando
    cmd = ultimo_comando.copy()
    ultimo_comando = {"accion": "ninguno"}
    return cmd


# ============================
# ESP32 ENVÍA SU ESTADO
# ============================
@app.post("/estado")
def recibir_estado(data: Estado):
    global estado_esp32
    estado_esp32 = data.dict()
    return {"status": "ok", "estado_actualizado": estado_esp32}


# ============================
# APP PIDE EL ESTADO DEL ESP32
# ============================
@app.get("/estado")
def obtener_estado():
    return estado_esp32
