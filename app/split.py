import boto3
import cv2
import os

class Split: 
    def __init__(self, video_data):
        # 비디오 데이터를 로컬 파일로 저장
        self.video_path = 'temp_video.mp4'
        with open(self.video_path, 'wb') as f:
            f.write(video_data)
        
    
    def capture_frames(self, output_dir, capture_times):
        # 비디오 파일 열기
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            return "비디오 파일을 열 수 없습니다."
        
        # 캡처할 시간 지정 (초)
        capture_seconds = capture_times
        
        # 이미지를 저장할 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)
        
        # 캡처된 시간과 프레임 번호 저장
        capture_frames = [(int(cap.get(cv2.CAP_PROP_FPS) * sec), sec) for sec in capture_seconds]
        
        # 프레임 캡처 및 이미지 저장
        frame_count = 0
        current_capture = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # 캡처할 시간에 해당하는 프레임 캡처 및 이미지 저장
            if frame_count == capture_frames[current_capture][0]:
                output_path = os.path.join(output_dir, f"frame_{capture_frames[current_capture][1]}.jpg")
                cv2.imwrite(output_path, frame)
                current_capture += 1
                if current_capture >= len(capture_frames):
                    break
                
            frame_count += 1
        
        cap.release()
        return "프레임 캡처가 완료되었습니다."