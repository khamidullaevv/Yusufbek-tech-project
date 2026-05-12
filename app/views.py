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
from .serializer import (
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
        student.save()
        balance.save()
        return Response({'student': StudentSerializer(student).data, 'balance': balance.amount})


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('student', 'group').order_by('-date')
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]
    filter_fields = ['student', 'group']
    search_fields = ['student_name']
    ordering_fields = ['date', 'amount']


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]
    search_fields = ['name']
    filter_fields = ['paid', 'color']

    @action(detail=True, methods=['post'])
    def toggle_paid(self, request, pk=None):
        expense = self.get_object()
        old_paid = expense.paid
        expense.paid = not expense.paid

        balance = Balance.objects.first() or Balance.objects.create()
        if not expense.paid and old_paid:
            balance.amount += expense.amount
        elif expense.paid and not old_paid:
            if balance.amount >= expense.amount:
                balance.amount -= expense.amount
            else:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        expense.save()
        balance.save()
        return Response({'expense': ExpenseSerializer(expense).data, 'balance': balance.amount})


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.select_related('group')
    serializer_class = HomeworkSerializer
    permission_classes = [AllowAny]
    filter_fields = ['group']
    search_fields = ['title']
    ordering_fields = ['deadline']


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    filter_fields = ['tag']
    search_fields = ['text']
    ordering_fields = ['date', 'likes']

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        news = self.get_object()
        news.likes += 1
        news.save()
        return Response({'likes': news.likes})


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('student', 'group')
    serializer_class = AttendanceSerializer
    permission_classes = [AllowAny]
    filter_fields = ['group', 'student', 'status', 'month']
    search_fields = ['student__name']
    ordering_fields = ['date']


class CustomScheduleViewSet(viewsets.ModelViewSet):
    queryset = CustomSchedule.objects.all()
    serializer_class = CustomScheduleSerializer
    permission_classes = [AllowAny]
    ordering_fields = ['day', 'time']