from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import datetime

from .models import (
    Balance, District, Teacher, Group, DistrictStudent, Student, Payment,
    Expense, Homework, News, Attendance, CustomSchedule
)
from .serializers import (
    BalanceSerializer, DistrictSerializer, TeacherSerializer, GroupSerializer,
    DistrictStudentSerializer, StudentSerializer, PaymentSerializer,
    ExpenseSerializer, HomeworkSerializer, NewsSerializer,
    AttendanceSerializer, CustomScheduleSerializer
)


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def add_payment(self, request):
        amount = request.data.get('amount', 0)
        balance = Balance.objects.first() or Balance.objects.create()
        balance.amount += int(amount)
        balance.save()
        return Response({'balance': balance.amount})

    @action(detail=False, methods=['post'])
    def withdraw(self, request):
        amount = request.data.get('amount', 0)
        balance = Balance.objects.first() or Balance.objects.create()
        if balance.amount >= int(amount):
            balance.amount -= int(amount)
            balance.save()
            return Response({'balance': balance.amount})
        return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.prefetch_related('students')
    serializer_class = DistrictSerializer
    permission_classes = [AllowAny]
    filter_fields = ['city']
    search_fields = ['name']
    ordering_fields = ['name']


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]
    search_fields = ['name', 'subject']
    ordering_fields = ['name', 'salary']
    filter_fields = ['status']


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.select_related('teacher')
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]
    search_fields = ['subject', 'id_code']
    filter_fields = ['level']


class DistrictStudentViewSet(viewsets.ModelViewSet):
    queryset = DistrictStudent.objects.select_related('district')
    serializer_class = DistrictStudentSerializer
    permission_classes = [AllowAny]
    filter_fields = ['district', 'status']
    search_fields = ['name']


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('group')
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    search_fields = ['name', 'phone']
    filter_fields = ['group', 'paid', 'direction']

    @action(detail=True, methods=['post'])
    def toggle_paid(self, request, pk=None):
        student = self.get_object()
        old_paid = student.paid
        student.paid = not student.paid

        balance = Balance.objects.first() or Balance.objects.create()
        if student.paid and not old_paid:
            balance.amount += student.amount
            Payment.objects.create(
                student=student,
                student_name=student.name,
                group=student.group,
                amount=student.amount,
                month=timezone.now().strftime('%B')
            )
        elif not student.paid and old_paid:
            balance.amount -= student.amount
