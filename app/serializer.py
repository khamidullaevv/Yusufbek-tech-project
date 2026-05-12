from rest_framework import serializers
from .models import (
    Balance, District, Teacher, Group, DistrictStudent, Student, Payment,
    Expense, Homework, News, Attendance, CustomSchedule
)


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = 'all'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = 'all'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = 'all'


class GroupSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.name', read_only=True)
    
    class Meta:
        model = Group
        fields = 'all'


class DistrictStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictStudent
        fields = 'all'


class StudentSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.id_code', read_only=True)
    
    class Meta:
        model = Student
        fields = 'all'


class PaymentSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.id_code', read_only=True)
    
    class Meta:
        model = Payment
        fields = 'all'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = 'all'


class HomeworkSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.id_code', read_only=True)
    
    class Meta:
        model = Homework
        fields = 'all'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = 'all'


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    group_name = serializers.CharField(source='group.id_code', read_only=True)
    
    class Meta:
        model = Attendance
        fields = 'all'


class CustomScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSchedule
        fields = 'all'