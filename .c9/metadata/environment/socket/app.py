{"filter":false,"title":"app.py","tooltip":"/socket/app.py","undoManager":{"mark":1,"position":1,"stack":[[{"start":{"row":0,"column":0},"end":{"row":14,"column":0},"action":"remove","lines":["import json","from fastapi import FastAPI, WebSocket","from mangum import Mangum","","app = FastAPI()","","@app.websocket(\"/\")","async def websocket_endpoint(websocket: WebSocket):","    await websocket.accept()","    while True:","        data = await websocket.receive_text()","        await websocket.send_text(f\"Message text was: {data}\")","","handler = Mangum(app)",""],"id":1},{"start":{"row":0,"column":0},"end":{"row":19,"column":0},"action":"insert","lines":["import json","from fastapi import FastAPI, WebSocket","from mangum import Mangum","","app = FastAPI()","","@app.websocket(\"/ws\")","async def websocket_endpoint(websocket: WebSocket):","    await websocket.accept()","    while True:","        try:","            data = await websocket.receive_text()","            # 메시지 처리 로직을 여기에 추가","            await websocket.send_text(f\"Message text was: {data}\")","        except WebSocketDisconnect:","            print(\"Client disconnected\")","            break","","handler = Mangum(app)",""]}],[{"start":{"row":0,"column":0},"end":{"row":19,"column":0},"action":"remove","lines":["import json","from fastapi import FastAPI, WebSocket","from mangum import Mangum","","app = FastAPI()","","@app.websocket(\"/ws\")","async def websocket_endpoint(websocket: WebSocket):","    await websocket.accept()","    while True:","        try:","            data = await websocket.receive_text()","            # 메시지 처리 로직을 여기에 추가","            await websocket.send_text(f\"Message text was: {data}\")","        except WebSocketDisconnect:","            print(\"Client disconnected\")","            break","","handler = Mangum(app)",""],"id":2,"ignore":true},{"start":{"row":0,"column":0},"end":{"row":18,"column":0},"action":"insert","lines":["import json","from fastapi import FastAPI, WebSocket, WebSocketDisconnect","from mangum import Mangum","","app = FastAPI()","","@app.websocket(\"/ws\")","async def websocket_endpoint(websocket: WebSocket):","    await websocket.accept()","    try:","        while True:","            data = await websocket.receive_text()","            # 수신한 메시지를 Lambda 함수로 전달하거나 로직을 추가합니다.","            await websocket.send_text(f\"Message text was: {data}\")","    except WebSocketDisconnect:","        print(\"Client disconnected\")","","handler = Mangum(app)",""]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":9,"column":8},"end":{"row":9,"column":8},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1716563409699,"hash":"16d64c291a0c6ee461033b48c350b84d79a181d5"}