from rest_framework import serializers

class EssayRequestSerializer(serializers.Serializer):
    student_id = serializers.CharField(max_length=8)
    student_name = serializers.CharField(max_length=10)
    department = serializers.CharField(max_length=20)
    application_type = serializers.CharField(max_length=10)
    ocr_text = serializers.CharField()
    file = serializers.CharField()
    evaluation_category_id = serializers.IntegerField()