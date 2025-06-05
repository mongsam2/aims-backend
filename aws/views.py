from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
import boto3
import os
import uuid
from datetime import datetime
from django.conf import settings
from rest_framework.response import Response


# Create your views here.
class SePresignedUrlView(APIView):
    def post(self, request):
        file_type = request.data.get("file_type")
        if file_type not in ("image/png", "application/pdf", "image/jpeg"):
            return ValidationError(
                "파일 형식은 다음과 같아야합니다: image/png, application/pdf, image/jpeg"
            )

        document_type = request.data.get("type")
        if document_type not in ("student_record", "essay", "document"):
            return ValidationError(
                "잘못된 서류 종류입니다: (student_record", "essay", "document)"
            )

        file_ext = file_type.split("/")[1]
        today = datetime.now()
        folder_path = today.strftime(f"{document_type}/%Y/%m/%d")
        s3_key = f"{folder_path}/{uuid.uuid4()}.{file_ext}"

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION_NAME,
        )

        presigned_post = s3_client.generate_presigned_post(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=s3_key,
            Fields={
                "Content-Type": file_type,
            },
            Conditions=[
                {"Content-Type": file_type},
            ],
            ExpiresIn=3600,
        )

        return Response(
            {
                "url": presigned_post["url"],
                "key": s3_key,  # 프론트가 업로드 후 저장할 경로 참조
            },
            status=200,
        )
