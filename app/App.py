import streamlit as st
from streamlit_option_menu import option_menu
from user import User
from url_submit import S3Url
from file_uploader import FileUploader
from split import Split
from s3 import S3
import plotly.express as px
import pandas as pd
import json
import requests
import json

st.title("🤖 X-men")
# 사이드바 구성
with st.sidebar:    
    # 메뉴 구성
    choice = option_menu("Menu", ["홈","데이터 업로드", "데이터 시각화"],
                         icons=['bi bi-house','bi bi-cloud-arrow-up','bi bi-bar-chart-line'],
                         menu_icon = "app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )

# 초기 세션 상태 설정
if 'ID' not in st.session_state:
    st.session_state.ID = ""
    
# 사용자 ID 입력 및 로그인
if choice == "홈":
    st.subheader("사용자 ID")
    user_id = st.text_input("", "")
    if st.button("로그인"):
        user = User(user_id)
        ID = user.login()
        if ID :
            st.session_state.ID = ID
            st.success("로그인되었습니다.")
        else :
            st.error("아이디를 입력해주세요.")

# 영상 & 이미지 업로드
elif choice == "데이터 업로드":
    # ID를 입력 받은 경우에만 업로드를 받기
    if st.session_state.ID: 
        st.subheader("데이터 업로드")
        # 정해져 있는 영상 선택
        st.write("⬆️영상을 선택해주세요") 
        # 버튼 가로로 배열 : 세 개의 열 생성
        col1, col2, col3 = st.columns(3)
        # s3에 있는 동영상 불러오기
        s3 = S3()
        bucket_name = 'xvideoset'
        local_file_path = 'downloaded_video.mp4'
        with col1:
            if st.button('1번 동영상'):
                file_key = 'videos/저장매체1.mp4'
                local_file = s3.stream_s3_file(bucket_name, file_key)
                # 이미지를 저장할 디렉토리 경로
                output_dir = 'captured_frames'
                # 캡처할 시간 지정 (초)
                capture_times = [5, 35, 75, 130, 150, 170, 220, 255, 310]
                # 프레임 캡처 실행
                split = Split(local_file)
                split.capture_frames(output_dir, capture_times)
                st.write("File streaming started")
                image_folder = 'captured_frames'
                urls = s3.upload_images_to_s3(image_folder, bucket_name, "video1")
                
                # 업로드된 이미지들의 URL 출력
                status, submit_message = S3Url(st.session_state.ID, urls).url_submit()
                if status == "success":
                    st.success(submit_message)
                else:
                    st.error(submit_message)
                    
                endpoint_url = ""

                # 엔드포인트에 POST 요청 보내기
                response = requests.post(endpoint_url)
                
                # 요청이 성공한 경우
                if response.status_code == 200:
                    prediction = response.json()
                    st.write(prediction)
        with col2:
            if st.button('2번 동영상'):
                file_key = 'videos/저장매체2.mp4'
                local_file = s3.stream_s3_file(bucket_name, file_key)
                # 이미지를 저장할 디렉토리 경로
                output_dir = 'captured_frames'
                # 캡처할 시간 지정 (초)
                capture_times = [0, 6, 30, 43, 68, 105, 137, 201, 228, 274, 304, 334]
                # 프레임 캡처 실행
                split = Split(local_file)
                split.capture_frames(output_dir, capture_times)
                st.write("File streaming started")
                image_folder = 'captured_frames'
                urls = s3.upload_images_to_s3(image_folder, bucket_name, "video2")
                
                # 업로드된 이미지들의 URL 출력
                status, submit_message = S3Url(st.session_state.ID, urls).url_submit()
                if status == "success":
                    st.success(submit_message)
                else:
                    st.error(submit_message)
                    
        with col3:       
            if st.button('3번 동영상'):
                file_key = 'videos/저장매체3.mp4'
                local_file = s3.stream_s3_file(bucket_name, file_key)
                # 이미지를 저장할 디렉토리 경로
                output_dir = 'captured_frames'
                # 캡처할 시간 지정 (초)
                capture_times = [5, 35, 75, 130, 150, 170, 220, 255, 310]
                # 프레임 캡처 실행
                split = Split(local_file)
                split.capture_frames(output_dir, capture_times)
                st.write("File streaming started")
                image_folder = 'captured_frames'
                urls = s3.upload_images_to_s3(image_folder, bucket_name, "video3")
                
                # 업로드된 이미지들의 URL 출력
                status, submit_message = S3Url(st.session_state.ID, urls).url_submit()
                if status == "success":
                    st.success(submit_message)
                else:
                    st.error(submit_message)
    
        uploaded_file = st.file_uploader("⬆️다른 이미지나 영상을 업로드해주세요", type=["jpg", "jpeg", "png", "mp4"])
        if uploaded_file is not None:
            file_uploader = FileUploader(st.session_state.ID,uploaded_file)
            
            if not file_uploader.is_image() and not file_uploader.is_video():
                st.error("올바른 파일 형식이 아닙니다. 이미지 또는 동영상 파일을 업로드하세요.")
            else:
                status, submit_message = file_uploader.upload_file()
                if status == "success":
                    st.success(submit_message)
                else:
                    st.error(submit_message)
                    
     # ID 입력을 받지 못한 경우 경고 문구를 보여준다.
    else :
        st.warning("로그인이 필요합니다. 홈에서 로그인해주세요.")
    
# 데이터 시각화
elif choice == "데이터 시각화":
    st.subheader("데이터 시각화")
    if st.button("📊당일 데이터 내역 확인하기"):
        # API Gateway 엔드포인트 URL
        API_ENDPOINT = ''
        
        AUTH_TOKEN = ''
        
        headers = {
            'Authorization': f'Bearer {AUTH_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        
        try:
            # API에 POST 요청 보내기
            response = requests.post(API_ENDPOINT, headers=headers)
            
            # 응답 상태코드 확인
            if response.status_code == 200:
                # 응답 데이터 추출
                data = response.json()
                data = json.loads(data["body"])
                if data is not None:
                    # 데이터 처리
                    categories = list(data.keys())
                    values = [data[category] for category in categories]
                    
                    # 데이터 정렬
                    sorted_data = sorted(zip(values, categories), reverse=True)
                    df = pd.DataFrame(sorted_data, columns=['Value', 'Category'])
                
                    # Plotly를 사용하여 막대 차트 생성
                    fig = px.bar(df, x='Category', y='Value',barmode='group')
                    
                    # 모든 막대의 색상을 동일하게 설정
                    fig.update_traces(marker_color='rgb(178,204,255)')
                    
                    # 차트 제목 설정
                    fig.update_layout(
                        title='Daily Detection Results Statistics'  # 차트 제목 설정
                    )
                     
                    # Streamlit에서 차트 표시
                    st.plotly_chart(fig)
                else :
                    st.error("Not data")
                    print("No data")
            else:
                print(f"API 호출에 실패했습니다. 상태 코드: {response.status_code}")

        except Exception as e:
            print(f"API 호출 중 오류 발생: {e}")
