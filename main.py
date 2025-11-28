from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

app = FastAPI()

# Guardará la conexión WebSocket del ESP32
esp32_ws: WebSocket | None = None


# ===========================
#  WEBSOCKET PARA EL ESP32
# ===========================
@app.websocket("/ws")
async def websocket_esp32(websocket: WebSocket):
    global esp32_ws

    await websocket.accept()
    esp32_ws = websocket
    print("ESP32 conectado")

    try:
        while True:
            data = await websocket.receive_text()
            print("ESP32 envió:", data)

    except WebSocketDisconnect:
        print("ESP32 desconectado")
        esp32_ws = None


# ===========================
#  FUNCIÓN PARA ENVIAR COMANDO AL ESP32
# ===========================
async def enviar_al_esp32(cmd: str):
    if esp32_ws is None:
        return False
    try:
        await esp32_ws.send_text(cmd)
        return True
    except:
        return False


# ===========================
#  API PUBLICA PARA TU CELULAR / HTML / APK
# ===========================
@app.get("/send/{cmd}")
async def send_command(cmd: str):

    enviado = await enviar_al_esp32(cmd)

    if not enviado:
        return JSONResponse(
            {"status": "error", "mensaje": "ESP32 no está conectado"},
            status_code=500
        )

    return {"status": "ok", "comando": cmd}


# ===========================
#  RUTAS ESPECIFICAS (OPCIONAL)
# ===========================
@app.get("/")
async def root():
    return {"mensaje": "API IoT funcionando"}


@app.get("/estado/esp32")
async def estado():
    return {"conectado": esp32_ws is not None}
