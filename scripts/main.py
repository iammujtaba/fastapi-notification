from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from notifications.services import EventLogger, websocker_manager

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Notification</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <h2>Incoming notifications:</h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        window.onload = function(){
            const url = window.location.href;
            const urlParams = new URLSearchParams(window.location.search);
            var user_id = urlParams.get("user_id")

            document.querySelector("#ws-id").textContent = user_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${user_id}`);
        }

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.get("/profile/{user_id}")
async def get(user_id:int):
    even = EventLogger(process_event=True)
    await even.log_event('User_Login', {'user_id':user_id,'username':'test_user'})
    return {"user_id":user_id}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocker_manager.connect(websocket,user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocker_manager.send_notification_to_client(user_id, f"You: {data}")
            await websocker_manager.broadcast_notification(user_id,message = f"Client #{user_id}: {data}")
    except WebSocketDisconnect:
        websocker_manager.disconnect(user_id)
        await websocker_manager.broadcast_notification(user_id,f"Client #{user_id} left the chat")
