# Views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework import status

# Serializers
from .serializers import EssaysSerializer, EssayDetailSerializer, EssayCriteriaListSerializer, EssayScoreSerializer

# Models
from .models import Essay, EssayCriteria, CriteriaItem, EssayScore
from students.models import Student
from common.models import DocumentType

# Utils
from utils.upstage import execute_ocr
from utils.essay import evaluate

# Exceptions
from rest_framework.exceptions import NotFound, NotAcceptable, ParseError

# Settings
from django.conf import settings


# Create your views here.
class EssaysView(GenericAPIView, CreateModelMixin, ListModelMixin):
    serializer_class = EssaysSerializer
    queryset = Essay.objects.filter(state="제출")

    def post(self, request):
        '''
        논술 답안지를 업로드하는 API
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
        
        # criteria 검증
        if not request.data.get('criteria'):
            raise ParseError("평가 항목을 선택해주세요.")
        
        # 기존에 제출 완료된 생기부가 존재 여부 검증
        if Essay.objects.filter(student=student, state="제출").exists():
            raise NotAcceptable(f"{id} 학생의 논술 답안지가 이미 제출되었습니다.")
        
        # DocumentType 검증
        try:
            document_type = DocumentType.objects.get(name='논술')
        except DocumentType.DoesNotExist:
            raise NotFound("DocumentType에서'논술'을 찾을 수 없습니다.")
        
        # Criteria
        criteria_id = request.data.get('criteria')
        try:
            criteria = EssayCriteria.objects.get(id=criteria_id)
        except EssayCriteria.DoesNotExist:
            raise NotFound(f"id:{criteria_id} 평가 항목을 찾을 수 없습니다.")
    
        api_key = settings.UPSTAGE_API_KEY
        
        # OCR 추출
        extraction = execute_ocr(api_key, file.file)
        evaluation, penalty = evaluate(api_key, extraction, criteria)
        
        return self.create(
            request, 
            student=student, 
            document_type=document_type, 
            extraction=extraction, 
            evaluation=evaluation,
            score_by_length=penalty,
            criteria=criteria,
            state="제출"
        )

    def get(self, request):
        '''
        제출된 논술 답안지 목록을 반환하는 API
        '''
        return self.list(request)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, *args, **kwargs)    
        headers = self.get_success_headers(serializer.data) 
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(**kwargs)


class EssayDetailView(RetrieveAPIView):
    serializer_class = EssayDetailSerializer
    queryset = Essay.objects.all()
    lookup_field = 'id'

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'essay_id': self.kwargs['id']
        }


class EssayCriteriasView(ListAPIView):
    serializer_class = EssayCriteriaListSerializer
    queryset = EssayCriteria.objects.all()
    lookup_field = 'id'


class EssayScoreView(APIView):
    def get_object(self, id):
        try:
            return Essay.objects.get(id=id)
        except Essay.DoesNotExist:
            raise NotFound(f"id:{id} 논술 답안지를 찾을 수 없습니다.")

    def post(self, request, id):
        essay = self.get_object(id)
        serializer = EssayScoreSerializer(data=request.data, many=True, context={'essay': essay})
        
        # 이미 평가를 한 상태인지 검증
        if essay.essay_scores.exists():
            raise NotAcceptable(f"{id} 논술 답안지의 평가 항목 점수가 이미 존재합니다.")

        if serializer.is_valid(raise_exception=True):
            # 평가항목의 개수가 일치하는지 검증
            if len(serializer.validated_data) != essay.criteria.criteria_items.count():
                raise ParseError("평가 항목의 개수가 일치하지 않습니다.")
            
            # 이미 채점을 한 상태인지 검증증
            essay_score_list = []
            for data in serializer.validated_data:
                essay_score_list.append(EssayScore(essay=essay, **data))
            EssayScore.objects.bulk_create(essay_score_list)
        return Response(f"{id} 논술 답안지의 {len(serializer.data)}개 항목 점수가 저장되었습니다.", status=status.HTTP_201_CREATED)