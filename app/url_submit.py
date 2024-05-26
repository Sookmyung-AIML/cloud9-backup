import requests
import json

class S3Url:
    def __init__(self, userID, urls):
        self.user_id = userID
        self.url_list = urls

    def url_submit(self):
        if self.user_id and self.url_list:
            # API Gateway 엔드포인트 URL
            api_url = 'https://349pm4hszk.execute-api.ap-northeast-2.amazonaws.com/Xmen_stage/xmen-test2'
        
            # 요청에 포함될 데이터
            data = {
                'body': json.dumps({
                    'UserID': self.user_id,
                    'urlList': self.url_list
                })
            }

        
            # POST 요청 보내기
            response = requests.post(api_url, json=data)
        
            # 응답 결과 출력 - (해당 결과, 문구) 반환
            if response.status_code == 200:
                return ("success", f"Analysis Result: {response.json()['body']}")
            else:
                return ("error", f"Error: {response.json()['body']}")
        else:
            return ("error", 'Please enter both User ID and Video Number.')
        