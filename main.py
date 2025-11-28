from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

app = FastAPI()

# Guardar conexiones
esp32_ws: WebSocket | None = None
app_ws: WebSocket | None = None


# =====================================
#   WEBSOCKET DEL ESP32
# =====================================
@app.websocket("/ws")
async def websocket_esp32(websocket: WebSocket):
    global esp32_ws
    await websocket.accept()
    esp32_ws = websocket
    print("ESP32 conectado!")

    try:
        while True:
            data = await websocket.receive_text()
            print("ESP32 dijo:", data)
            # (Opcional: reenviar datos al APP)
            if app_ws:
                await app_ws.send_text(f"ESP32:{data}")

    except WebSocketDisconnect:
        print("ESP32 desconectado")
        esp32_ws = None


# =====================================
#   WEBSOCKET DEL APP (Flutter)
# =====================================
@app.websocket("/app")
async def websocket_app(websocket: WebSocket):
    global app_ws
    await websocket.accept()
    app_ws = websocket
    print("Flutter conectado!")

    try:
        while True:
            cmd = await websocket.receive_text()
            print("Flutter envió:", cmd)

            # Reenviar comando al ESP32
            if esp32_ws:
                await esp32_ws.send_text(cmd)
            else:
                await websocket.send_text("ERROR: ESP32 no conectado")

    except WebSocketDisconnect:
        print("Flutter desconectado")
        app_ws = None


# =====================================
#   API HTTP PARA PRUEBAS DESDE EL NAVEGADOR
# =====================================
@app.get("/send/{cmd}")
async def send_command(cmd: str):
    if esp32_ws is None:
        return JSONResponse({"status": "error", "mensaje": "ESP32 no conectado"}, status_code=500)

    try:
        await esp32_ws.send_text(cmd)
        return {"status": "ok", "comando": cmd}
    except:
        return JSONResponse({"status": "error", "mensaje": "Error enviando al ESP32"}, status_code=500)


@app.get("/")
async def root():
    return {"status": "OK", "message": "Servidor IoT funcionando"}

@app.get("/estado")
async def estado():
    return {
        "ESP32": esp32_ws is not None,
        "Flutter": app_ws is not None
    }
