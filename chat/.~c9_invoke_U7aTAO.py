import streamlit as st
import json
import requests
import time
from PIL import Image
import websockets
import asyncio
import threading
import boto3
import io

st.title("💬 AI SERVICE")

# AWS 자격 증명 설정
aws_access_key_id = "YOUR_AWS_ACCESS_KEY_ID"
aws_secret_access_key = "YOUR_AWS_SECRET_ACCESS_KEY"

# S3 클라이언트 초기화
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='ap-northeast-2'  # AWS 리전을 지정합니다.
)

@st.cache_resource
def get_event_loop():
    return asyncio.new_event_loop()

async def on_message(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get('action')
            
            if action == 'start_scanning':
                st.session_state.stage = 1
                st.session_state.messages.append({"role": "assistant", "content": "스캔을 시작합니다. 잠시만 기다려 주세요..."})
            
            elif action == 'scan_complete':
                st.session_state.stage = 2
                result = data.get('result', {})
                st.session_state.detection_results = result
                st.session_state.messages.append({"role": "assistant", "content": "스캔이 완료되었습니다."})
            
            st.experimental_rerun()
    except Exception as e:
        st.error(f"Error in on_message: {str(e)}")

async def websocket_loop():
    try:
        ws_url = "wss://md7zor4opa.execute-api.ap-northeast-2.amazonaws.com/dev"
        async with websockets.connect(ws_url) as websocket:
            st.session_state.ws = websocket
            await on_message(websocket)
    except Exception as e:
        st.error(f"Error in websocket_loop: {str(e)}")

def start_websocket_loop():
    asyncio.run(websocket_loop())

# 세션 상태 초기화
if "ws" not in st.session_state:
    st.session_state.ws = None
if "ws_thread" not in st.session_state:
    st.session_state.ws_thread = threading.Thread(target=start_websocket_loop, daemon=True)
    st.session_state.ws_thread.start()
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요.<br>가방을 눕혀서 올려주세요."}
    ]
if "detection_results" not in st.session_state:
    st.session_state.detection_results = None
if "show_image" not in st.session_state:
    st.session_state.show_image = False
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

# 메시지 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"], unsafe_allow_html=True)

# 업로드된 이미지를 화면에 표시
if st.session_state.stage == 0:
    if st.button('Start Scanning'):
        if st.session_state.ws and st.session_state.ws.open:
            st.write("Sending start_scanning message...")
            asyncio.run(st.session_state.ws.send(json.dumps({"action": "start_scanning", "userId": "test_user", "videoNumber": "1"})))
        else:
            st.error("WebSocket 연결이 닫혀 있습니다. 다시 시도해 주세요.")
            st.session_state.ws_thread = threading.Thread(target=start_websocket_loop, daemon=True)
            st.session_state.ws_thread.start()
        st.experimental_rerun()

elif st.session_state.stage == 1:
    st.session_state.messages.append({"role": "assistant", "content": "스캔 결과를 기다리는 중입니다. 잠시만 기다려 주세요..."})
    st.chat_message("assistant").write("스캔 결과를 기다리는 중입니다. 잠시만 기다려 주세요...")

elif st.session_state.stage == 2:
    detection_results = st.session_state.get('detection_results', None)
    if detection_results:
        def get_position_text(positions):
            position_texts = []
            if positions[0] > 0:
                position_texts.append(f"왼쪽 상단에 {positions[0]}개")
            if positions[1] > 0:
                position_texts.append(f"오른쪽 상단에 {positions[1]}개")
            if positions[2] > 0:
                position_texts.append(f"왼쪽 하단에 {positions[2]}개")
            if positions[3] > 0:
                position_texts.append(f"오른쪽 하단에 {positions[3]}개")
            return ", ".join(position_texts)

        def generate_detection_message(detection_results):
            total_objects = sum([obj["amount"] for obj in detection_results["objects"]])
            detection_message = f"총 {total_objects}개의 물품이 탐지되었습니다.\n"
            for obj in detection_results["objects"]:
                detection_message += f"<br>{obj['type']}가 {obj['amount']}개 탐지되었습니다.\n"
                position_text = get_position_text(obj["position"])
                detection_message += f"<br>{obj['type']}는 {position_text}로 예상됩니다.\n"
            return detection_message
        
        detection_message = generate_detection_message(detection_results)
        st.session_state.messages.append({"role": "assistant", "content": detection_message})
        st.chat_message("assistant").write(detection_message)
        
        s3_url = detection_results["s3"]
        bucket_name, key = s3_url.replace("s3://", "").split("/", 1)
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        img = Image.open(io.BytesIO(response['Body'].read()))
        st.session_state.uploaded_image = img
        st.session_state.show_image = True
        st.session_state.stage = 3
        st.experimental_rerun()

elif st.session_state.stage == 3:
    if st.session_state.show_image and st.session_state.uploaded_image:
        st.image(st.session_state.uploaded_image, caption='Detected Objects', use_column_width=True)
    else:
        st.error("Error: Could not load the image from the provided S3 URL.")

    st.session_state.messages.append({"role": "assistant", "content": "확인을 완료했습니다. 감사합니다."})
    st.chat_message("assistant").write("확인을 완료했습니다. 감사합니다.")
    st.session_state.stage = 4
    st.experimental_rerun()

elif st.session_state.stage == 4:
    if st.button('Retry Scanning'):
        st.session_state.messages.append({"role": "user", "content": "Retry Scanning"})
        st.session_state.messages.append({"role": "assistant", "content": "다시 스캔을 시작합니다. 잠시만 기다려 주세요..."})
        st.chat_message("assistant").write("다시 스캔을 시작합니다. 잠시만 기다려 주세요...")
        st.session_state.stage = 1
        st.experimental_rerun()
    if st.button('Complete'):
        st.session_state.messages.append({"role": "user", "content": "Complete"})
        st.session_state.messages.append({"role": "assistant", "content": "확인을 완료했습니다. 감사합니다."})
        st.chat_message("assistant").write("확인을 완료했습니다. 감사합니다.")

def main():
    pass

if __name__ == '__main__':
    main()
