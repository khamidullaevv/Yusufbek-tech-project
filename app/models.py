from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Ustoz'),
        ('student', 'Oquvchi'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Guruh nomi")
    teacher = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'role': 'teacher'},
        verbose_name="Ustoz"
    )
    students = models.ManyToManyField(
        User, 
        related_name='student_groups', 
        limit_choices_to={'role': 'student'},
        verbose_name="Oquvchi"
    )

    def __str__(self):
        return self.name

class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата занятия")
    is_present = models.BooleanField(default=False, verbose_name="Darsda qatnashgan")

    class Meta:
        unique_together = ('student', 'group', 'date') 

class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="To'lov miqdori")
    date_paid = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=255, blank=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title