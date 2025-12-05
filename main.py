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
    luces: str | None = None


# ============================
# VARIABLES GLOBALES
# ============================
ultimo_comando = {"accion": "ninguno"}

estado_esp32 = {
    "temp": 0.0,
    "hum": 0.0,
    "puerta": "desconocido",
    "garage": "desconocido",
    "luces": "desconocido"
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
    """
    Guarda el comando enviado por la app.
    El ESP32 lo leerá una sola vez.
    """
    global ultimo_comando
    ultimo_comando = {"accion": cmd.accion}
    return {"status": "ok", "accion_guardada": cmd.accion}


# ============================
# ESP32 PIDE EL COMANDO → ENTREGAR Y BORRAR
# ============================
@app.get("/comando")
def enviar_comando():
    """
    El ESP32 obtiene el comando pendiente.
    Luego se borra para que no se repita.
    """
    global ultimo_comando
    cmd = ultimo_comando.copy()
    ultimo_comando = {"accion": "ninguno"}  # prevenir repetición
    return cmd


# ============================
# ESP32 ENVÍA SU ESTADO
# ============================
@app.post("/estado")
def recibir_estado(data: Estado):
    """
    El ESP32 actualiza su estado cada 1 segundo.
    """
    global estado_esp32
    estado_esp32 = data.dict()
    return {"status": "ok", "estado_actualizado": estado_esp32}


# ============================
# APP PIDE EL ESTADO DEL ESP32
# ============================
@app.get("/estado")
def obtener_estado():
    """
    La app obtiene el estado más reciente enviado por el ESP32.
    """
    return estado_esp32
