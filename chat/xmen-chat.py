import streamlit as st
import json
import asyncio
import websockets
import threading
import boto3
import io
import time
from PIL import Image
from streamlit.runtime.scriptrunner import add_script_run_ctx

st.title("💬 AI SERVICE")

# AWS 자격 증명 설정
aws_access_key_id = ""
aws_secret_access_key = ""

# S3 클라이언트 초기화
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name='ap-northeast-2'  # AWS 리전을 지정합니다.
)

bucket_name = 'xvideoset'
prefix = 'video2_detect_2/'

async def on_message(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get('action')
            
            if action == 'start_scanning':
                st.session_state.stage = 1
                st.session_state.messages.append({"role": "assistant", "content": "스캔을 시작합니다. 잠시만 기다려 주세요..."})
                with st.spinner("스캔 중..."):
                    time.sleep(5)
                st.experimental_rerun()
            
            elif action == 'scan_complete':
                st.session_state.stage = 2
                result = data.get('result', {})
                st.session_state.detection_results = result
                st.session_state.messages.append({"role": "assistant", "content": "스캔이 완료되었습니다."})
                await handle_result(result["index"])  # WebSocket으로부터 받은 결과 처리
    except Exception as e:
        st.error(f"Error in on_message: {str(e)}")

async def websocket_loop():
    try:
        ws_url = "wss://sa79u8gqgf.execute-api.ap-northeast-2.amazonaws.com/production"
        async with websockets.connect(ws_url) as websocket:
            st.session_state.ws = websocket
            st.session_state.websocket_connected = True
            st.write("WebSocket 연결 성공!")  # 연결 성공 메시지 추가
            await on_message(websocket)
    except Exception as e:
        st.session_state.websocket_connected = False
        st.error(f"Error in websocket_loop: {str(e)}")

def start_websocket():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_loop())

def fetch_s3_data(index):
    json_key = f"{prefix}detection_results_{index}.json"
    png_key = f"{prefix}detection_results_{index}.png"
    
    json_object = s3_client.get_object(Bucket=bucket_name, Key=json_key)
    png_object = s3_client.get_object(Bucket=bucket_name, Key=png_key)
    
    json_data = json.loads(json_object['Body'].read().decode('utf-8'))
    png_data = Image.open(io.BytesIO(png_object['Body'].read()))
    
    return json_data, png_data

async def handle_result(index):
    st.session_state.messages = []  # 메시지 초기화
    st.session_state.show_buttons = False  # 버튼 숨기기
    json_data, png_data = fetch_s3_data(index)
    
    if not json_data:
        st.session_state.messages.append({"role": "assistant", "content": "반입 금지 물품이 탐지되지 않았습니다."})
        st.session_state.show_image = True
        st.session_state.uploaded_image = png_data
        st.experimental_rerun()
        await asyncio.sleep(2)
        st.session_state.messages.append({"role": "assistant", "content": "가방을 흔들어서 다시 한번 더 스캔해주세요."})
        st.session_state.show_retry_button = True
        st.experimental_rerun()
    else:
        with st.spinner("스캔 중..."):
                    time.sleep(5)
        result_message = ", ".join([f"{key} {value}개" for key, value in json_data.items()])
        st.session_state.messages.append({"role": "assistant", "content": f"{result_message} 발견되었습니다."})
        st.session_state.show_image = True
        st.session_state.uploaded_image = png_data
        st.experimental_rerun()
        await asyncio.sleep(2)
        st.session_state.messages.append({"role": "assistant", "content": "반입 금지 물품은 제거 부탁드립니다. 감사합니다."})
        st.session_state.show_retry_button = True
        st.experimental_rerun()

# 세션 상태 초기화
if "ws" not in st.session_state:
    st.session_state.ws = None
if "websocket_connected" not in st.session_state:
    st.session_state.websocket_connected = False
if "ws_thread" not in st.session_state:
    st.session_state.ws_thread = threading.Thread(target=start_websocket, daemon=True)
    add_script_run_ctx(st.session_state.ws_thread)
    st.session_state.ws_thread.start()
# 세션 상태 초기화
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
if "show_buttons" not in st.session_state:
    st.session_state.show_buttons = True
if "show_retry_button" not in st.session_state:
    st.session_state.show_retry_button = False

# WebSocket 연결 상태 표시
if st.session_state.websocket_connected:
    st.success("WebSocket 연결 성공!")
else:
    st.warning("WebSocket 연결 대기 중...")

# 메시지 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"], unsafe_allow_html=True)

# 업로드된 이미지를 화면에 표시
if st.session_state.show_buttons:
    cols = st.columns(5)  # 버튼을 가로로 배치하기 위해 5개의 열 생성
    for i in range(1, 10):
        col = cols[(i-1) % 5]  # 각 열에 버튼을 순서대로 배치
        with col:
            if st.button(f"{i}번 결과 확인"):
                asyncio.run(handle_result(i-1))  # 인덱스는 0부터 시작하므로 i-1

if st.session_state.show_image and st.session_state.uploaded_image:
    st.image(st.session_state.uploaded_image, caption='Detected Objects', use_column_width=True)
    st.chat_message("assistant").write("반입 금지 물품은 제거 부탁드립니다. 감사합니다.")

if st.session_state.show_retry_button:
    if st.button('Retry Scanning'):
        st.session_state.messages = []  # 메시지 초기화
        st.session_state.messages.append({"role": "user", "content": "Retry Scanning"})
        st.session_state.messages.append({"role": "assistant", "content": "다시 스캔을 시작합니다. 잠시만 기다려 주세요..."})
        st.chat_message("assistant").write("다시 스캔을 시작합니다. 잠시만 기다려 주세요...")
        st.session_state.show_buttons = True  # 버튼 다시 보이기
        st.session_state.show_retry_button = False
        st.experimental_rerun()
    if st.button('Complete'):
        st.session_state.messages = []  # 메시지 초기화
        st.session_state.messages.append({"role": "user", "content": "Complete"})
        st.session_state.messages.append({"role": "assistant", "content": "확인을 완료했습니다. 감사합니다."})
        st.chat_message("assistant").write("확인을 완료했습니다. 감사합니다.")
        st.session_state.show_buttons = True  # 버튼 다시 보이기
        st.session_state.show_retry_button = False

def main():
    pass

if __name__ == '__main__':
    main()
