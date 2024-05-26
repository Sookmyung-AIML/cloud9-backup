{"changed":true,"filter":false,"title":"s3_uploader.py","tooltip":"/app/s3_uploader.py","value":"import requests\nimport json\n\nclass S3Url:\n    def __init__(self, userID, urls):\n        self.user_id = userID\n        self.url_list = urls\n\n    def url_submit(self):\n        if self.user_id and self.url_list:\n            # API Gateway 엔드포인트 URL\n            api_url = 'https://349pm4hszk.execute-api.ap-northeast-2.amazonaws.com/Xmen_stage/xmen_test'\n        \n            # 요청에 포함될 데이터\n            data = {\n                'body': json.dumps({\n                    'UserID': self.user_id,\n                    'urlList': self.url_list\n                })\n            }\n\n        \n            # POST 요청 보내기\n            response = requests.post(api_url, json=data)\n        \n            # 응답 결과 출력 - (해당 결과, 문구) 반환\n            if response.status_code == 200:\n                return (\"success\", f\"Analysis Result: {response.json()['body']}\")\n            else:\n                return (\"error\", f\"Error: {response.json()['body']}\")\n        else:\n            return (\"error\", 'Please enter both User ID and Video Number.')","undoManager":{"mark":-2,"position":1,"stack":[[{"start":{"row":3,"column":15},"end":{"row":3,"column":16},"action":"remove","lines":["r"],"id":62},{"start":{"row":3,"column":14},"end":{"row":3,"column":15},"action":"remove","lines":["e"]},{"start":{"row":3,"column":13},"end":{"row":3,"column":14},"action":"remove","lines":["d"]},{"start":{"row":3,"column":12},"end":{"row":3,"column":13},"action":"remove","lines":["a"]},{"start":{"row":3,"column":11},"end":{"row":3,"column":12},"action":"remove","lines":["o"]},{"start":{"row":3,"column":10},"end":{"row":3,"column":11},"action":"remove","lines":["l"]},{"start":{"row":3,"column":9},"end":{"row":3,"column":10},"action":"remove","lines":["p"]}],[{"start":{"row":3,"column":9},"end":{"row":3,"column":10},"action":"insert","lines":["r"],"id":63},{"start":{"row":3,"column":10},"end":{"row":3,"column":11},"action":"insert","lines":["l"]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":10,"column":9},"end":{"row":10,"column":9},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1716486340103}