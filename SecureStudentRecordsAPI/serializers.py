from rest_framework import serializers
from .models import StudentRecord

class StudentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRecord
        fields = ['id', 'owner', 'full_name', 'course', 'year_level']
        read_only_fields = ['owner']  # owner is set automatically, not by user input