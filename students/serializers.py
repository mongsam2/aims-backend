from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Student, ApplicantType

class StudentListSerializer(ModelSerializer):
    documents = SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'name', 'department', 'phone', 'applicant_type', 'documents')

    def get_documents(self, student):
        answer = dict()

        required_documents = student.required_documents.values_list('name', flat=True)
        for document_type in required_documents:
            if student.documents.filter(document_type=document_type, state="제출").exists():
                answer[document_type] = "제출"
            elif student.documents.filter(document_type=document_type, state="검토").exists():
                answer[document_type] = "검토"
            else:
                answer[document_type] = "미제출"

        if "학생생활기록부" in required_documents:
            if student.student_records.filter(state='제출').exists():
                answer["학생생활기록부"] = "제출"
            elif student.student_records.filter(state='검토').exists():
                answer["학생생활기록부"] = "검토"
            else:
                answer["학생생활기록부"] = "미제출"

        if "논술" in required_documents:
            if student.essays.filter(state='제출').exists():
                answer["논술"] = "제출"
            elif student.essays.filter(state='검토').exists():
                answer["논술"] = "검토"
            else:
                answer["논술"] = "미제출"
        
        return answer

class ApplicantTypesSerializer(ModelSerializer):
    class Meta:
        model = ApplicantType
        fields = ('id', 'name')