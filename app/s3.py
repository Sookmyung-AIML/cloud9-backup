import boto3
import numpy as np
import os

class S3:
    def __init__(self):
        # 환경 변수로 AWS 자격 증명 설정
        os.environ['AWS_ACCESS_KEY_ID'] = ''
        os.environ['AWS_SECRET_ACCESS_KEY'] = ''
        os.environ['AWS_DEFAULT_REGION'] = ''
        
        # S3와 상호작용을 위한 boto3 클라이언트 생성
        self.s3_client = boto3.client('s3')

    def stream_s3_file(self, bucket_name, file_key):
        # S3 객체를 스트리밍 방식으로 읽기
        s3_object = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
        return s3_object['Body'].read()
        
    def upload_images_to_s3(self,image_folder,bucket_name, image_url):
        urls = []
        
        for image_name in os.listdir(image_folder):
            if image_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 이미지 파일 필터링
                file_path = os.path.join(image_folder, image_name)
                try:
                    image_name = f'{image_url}/{image_name}'
                    self.s3_client.upload_file(file_path, bucket_name, image_name)
                    url = f"https://{bucket_name}.s3.amazonaws.com/{image_name}"
                    urls.append(url)
                except FileNotFoundError:
                    print(f"The file {file_path} was not found")

        return urls
