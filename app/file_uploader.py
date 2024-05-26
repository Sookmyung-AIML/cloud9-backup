import requests

class FileUploader:
    def __init__(self, userID, uploaded_file):
        self.user_id = userID
        self.uploaded_file = uploaded_file
        self.mime_type = uploaded_file.type
        self.file_data = uploaded_file.getvalue()
    
    def is_image(self):
        return self.mime_type.startswith('image')
    
    def is_video(self):
        return self.mime_type.startswith('video')
    
    def upload_file(self):
        if self.user_id and self.uploaded_file:
            # API Gateway 엔드포인트 URL
            api_url = 'https://your-api-gateway-endpoint.amazonaws.com/prod/your-lambda-function'
            
            # 파일 형식에 따라 저장
            file_type = "image" if self.is_image() else "video"
            files = {"file": (f"{file_type}_file", self.file_data, "multipart/form-data")}

            # 요청에 포함될 데이터
            files = {
                "file": (self.uploaded_file.name, self.file_data, self.mime_type)
            }

            # 요청에 포함될 데이터
            data = {
                'UserID': self.user_id
            }

            # POST 요청 보내기
            response = requests.post(api_url, data=data, files=files)
            
            # 응답 결과 출력
            if response.status_code == 200:
                return ("success", "The file has been successfully transmitted.")
            else:
                return ("error", "Error: An error occurred during file transmission.")
        else:
            return ("error", 'Please enter both User ID and Video & Image.')