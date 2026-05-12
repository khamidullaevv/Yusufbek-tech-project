from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

class Balance(models.Model):
    amount = models.BigIntegerField(default=0, verbose_name=_("Amount"))
    last_updated = models.DateTimeField(auto_now=True, verbose_name=_("Last Updated"))

    class Meta:
        verbose_name = _("Balance")
        verbose_name_plural = _("Balance")

    def __str__(self):
        return f"Balance: {self.amount}"

class District(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("District Name"))
    city = models.CharField(max_length=255, default="Toshkent", verbose_name=_("City"))

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return self.name

class DistrictStudent(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    age = models.IntegerField(validators=[MinValueValidator(5)], verbose_name=_("Age"))
    direction = models.CharField(max_length=100, verbose_name=_("Direction"))
    status = models.CharField(max_length=20, default='active', verbose_name=_("Status"))

    class Meta:
        verbose_name = _("District Student")
        verbose_name_plural = _("District Students")

class Teacher(models.Model):
    STATUS_CHOICES = [('active', _('Active')), ('inactive', _('Inactive'))]
    name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    salary = models.BigIntegerField(validators=[MinValueValidator(0)], verbose_name=_("Salary"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name=_("Status"))

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return self.name

class Group(models.Model):
    id_code = models.CharField(max_length=50, unique=True, primary_key=True, verbose_name=_("Group ID"))
    subject = models.CharField(max_length=255, verbose_name=_("Subject"))
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, verbose_name=_("Teacher"))
    room = models.CharField(max_length=50, verbose_name=_("Room"))
    time = models.TimeField(verbose_name=_("Time"))
    level = models.CharField(max_length=50, verbose_name=_("Level"))

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return self.id_code

class Student(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    phone = models.CharField(max_length=20, verbose_name=_("Phone"))
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name=_("Group"))
    direction = models.CharField(max_length=100, verbose_name=_("Direction"))
    paid = models.BooleanField(default=False, verbose_name=_("Is Paid"))
    amount = models.BigIntegerField(default=0, verbose_name=_("Fee Amount"))

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_("Student"))
    student_name = models.CharField(max_length=255, verbose_name=_("Student Name"))
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, verbose_name=_("Group"))
    amount = models.BigIntegerField(verbose_name=_("Amount"))
    date = models.DateField(auto_now_add=True, verbose_name=_("Date"))
    month = models.CharField(max_length=50, verbose_name=_("Month"))

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

class Expense(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    amount = models.BigIntegerField(verbose_name=_("Amount"))
    paid = models.BooleanField(default=False, verbose_name=_("Paid"))
    color = models.CharField(max_length=20, verbose_name=_("Color"))

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")

class Homework(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_("Group"))
    deadline = models.DateField(verbose_name=_("Deadline"))

    class Meta:
        verbose_name = _("Homework")
        verbose_name_plural = _("Homeworks")

class News(models.Model):
    text = models.TextField(verbose_name=_("Content"))
    tag = models.CharField(max_length=50, verbose_name=_("Tag"))
    likes = models.IntegerField(default=0, verbose_name=_("Likes"))
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name=_("Student"))
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name=_("Group"))
    date = models.DateField(verbose_name=_("Date"))
    status = models.CharField(max_length=20, verbose_name=_("Status"))
    month = models.IntegerField(verbose_name=_("Month"))

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendance")

class CustomSchedule(models.Model):
    day = models.DateField(verbose_name=_("Day"))
    time = models.TimeField(verbose_name=_("Time"))
    description = models.CharField(max_length=255, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Custom Schedule")
        verbose_name_plural = _("Custom Schedules")