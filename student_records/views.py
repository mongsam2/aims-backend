# Views
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status

# Serializers
from .serializers import StudentRecordsSerializer, StudentRecordDetailSerializer, StudentRecordMemoSerializer

# Models
from .models import StudentRecord, Summarization
from students.models import Student
from common.models import DocumentType

# Utils
from utils.upstage import execute_ocr
from utils.student_record import summarization_content, summarization_question

# Exceptions
from rest_framework.exceptions import NotFound, NotAcceptable, ParseError

# Settings
from django.conf import settings

# Create your views here.
class StudentRecordsView(GenericAPIView, CreateModelMixin, ListModelMixin):
    serializer_class = StudentRecordsSerializer
    queryset = StudentRecord.objects.filter(state="제출")

    def get(self, request):
        '''
        제출된 학생생활기록부 목록을 반환하는 API
        '''
        return self.list(request)

    def post(self, request):
        '''
        학생생활기록부를 업로드하는 API
            - 파일 이름에 들어있는 수험번호가 현재 존재하지 않으면 404 에러를 반환
        '''
        file = request.data.get('file')
        if not file:
            raise ParseError("파일을 첨부해주세요.")
        splited_file_name = file.name.split('_')
        if len(splited_file_name) != 2:
            raise NotAcceptable("파일 이름이 올바르지 않습니다.")
        id, _ = splited_file_name

        # 수험번호 검증
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            raise NotFound(f"{id} 학생을 DB에서 찾을 수 없습니다.")
        
        # 기존에 제출 완료된 생기부가 존재 여부 검증
        if StudentRecord.objects.filter(student=student, state="제출").exists():
            raise NotAcceptable(f"{id} 학생의 생기부가 이미 제출되었습니다.")
        
        # DocumentType 검증
        try:
            document_type = DocumentType.objects.get(name='학생생활기록부')
        except DocumentType.DoesNotExist:
            raise NotFound("DocumentType에서'학생생활기록부'을 찾을 수 없습니다.")
        
        api_key = settings.UPSTAGE_API_KEY

        # OCR 추출
        extraction = execute_ocr(api_key, file.file)

        # 생기부 요약, 질문 추출
        content = summarization_content(extraction, api_key)
        question = summarization_question(extraction, api_key)
        summarization = Summarization.objects.create(content=content, question=question)
        
        return self.create(
            request, 
            student=student, 
            document_type=document_type, 
            extraction=extraction, 
            summarization=summarization,
            state="제출"
        )


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, *args, **kwargs)    
        headers = self.get_success_headers(serializer.data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(**kwargs)

class StudentRecordDetailView(RetrieveUpdateAPIView):
    serializer_class = StudentRecordDetailSerializer
    queryset = StudentRecord.objects.all()
    lookup_field = 'id'
    http_method_names = ['get']

class StudentRecordMemoView(UpdateAPIView):
    serializer_class = StudentRecordMemoSerializer
    queryset = StudentRecord.objects.all()
    lookup_field = 'id'
    http_method_names = ['patch']