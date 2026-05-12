from django.db import models
from django.core.validators import MinValueValidator

class Balance(models.Model):
    """Касса - главный учет финансов"""
    amount = models.BigIntegerField(default=15750000, help_text="Сумма в сум")
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Касса"
        verbose_name_plural = "Касса"

    def __str__(self):
        return f"Баланс: {self.amount}"


class District(models.Model):
    """Районы города"""
    name = models.CharField(max_length=255)  # "Chilonzor tumani"
    city = models.CharField(max_length=255, default="Toshkent")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Район"
        verbose_name_plural = "Районы"
        ordering = ['name']

    def str(self):
        return f"{self.name}, {self.city}"


class Teacher(models.Model):
    """Преподаватели"""
    STATUS_CHOICES = [('active', 'Активный'), ('inactive', 'Неактивный')]
    
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)  # Предмет
    salary = models.BigIntegerField(validators=[MinValueValidator(0)])
    join_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['-created_at']

    def str(self):
        return f"{self.name} ({self.subject})"


class Group(models.Model):
    """Учебные группы"""
    LEVEL_CHOICES = [('begin', 'Начальный'), ('mid', 'Средний'), ('advanced', 'Продвинутый')]
    DAYS_CHOICES = [(0, 'Пн'), (1, 'Вт'), (2, 'Ср'), (3, 'Чт'), (4, 'Пт'), (5, 'Сб'), (6, 'Вс')]
    
    id_code = models.CharField(max_length=50, unique=True, primary_key=True)  # Frontend-1001
    subject = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.CharField(max_length=50)
    days = models.JSONField(default=list)  # [0, 2, 4] = Пн, Ср, Пт
    time = models.TimeField()
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='begin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
        ordering = ['id_code']

    def str(self):
        return f"{self.id_code} — {self.subject}"


class DistrictStudent(models.Model):
    """Студенты в районе (для статистики)"""
    STATUS_CHOICES = [('active', 'Активный'), ('inactive', 'Неактивный')]
    
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='students')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    age = models.IntegerField(validators=[MinValueValidator(5)])
    direction = models.CharField(max_length=100)  # Frontend, React, Node.js
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Студент района"
        verbose_name_plural = "Студенты района"

    def str(self):
        return f"{self.name} ({self.district.name})"


class Student(models.Model):
    """Студенты"""
    id_num = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    direction = models.CharField(max_length=100)  # Frontend, React, Node.js
    paid = models.BooleanField(default=False)
    amount = models.BigIntegerField(default=0, validators=[MinValueValidator(0)])
    join_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['-created_at']

def str(self):
        return f"{self.name} ({self.group})"


class Payment(models.Model):
    """Платежи от студентов"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    student_name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.BigIntegerField(validators=[MinValueValidator(0)])
    date = models.DateField(auto_now_add=True)
    month = models.CharField(max_length=50)  # "Апрель", "April"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-date']

    def str(self):
        return f"{self.student_name} — {self.amount} (от {self.date})"


class Expense(models.Model):
    """Расходы (электричество, вода, интернет, аренда)"""
    COLOR_CHOICES = [('y', 'Желтый'), ('a', 'Синий'), ('g', 'Зеленый'), ('pu', 'Фиолетовый')]
    
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=50)  # bolt, drop, wifi, rent
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    amount = models.BigIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"

    def str(self):
        return f"{self.name} ({self.amount})"


class Homework(models.Model):
    """Домашние задания"""
    title = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='homeworks')
    description = models.TextField()
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Домашнее задание"
        verbose_name_plural = "Домашние задания"
        ordering = ['deadline']

    def str(self):
        return f"{self.title} ({self.group})"


class News(models.Model):
    """Новости центра"""
    TAG_CHOICES = [
        ('info', 'Информация'),
        ('event', 'Мероприятие'),
        ('alert', 'Важно'),
        ('announce', 'Объявление')
    ]
    
    text = models.TextField()
    tag = models.CharField(max_length=20, choices=TAG_CHOICES)
    author = models.CharField(max_length=255, default='Admin')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-date', '-time']

    def str(self):
        return f"{self.text[:50]}..."


class Attendance(models.Model):
    """Данные по посещаемости"""
    STATUS_CHOICES = [
        ('present', 'Присутствовал'),
        ('absent', 'Отсутствовал'),
        ('late', 'Опоздал'),
        ('dayoff', 'Выходной')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    month = models.IntegerField()  # 0-11
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Посещаемость"
        verbose_name_plural = "Посещаемость"
        ordering = ['-date']
        unique_together = ['student', 'group', 'date']

    def str(self):
        return f"{self.student} — {self.status} ({self.date})"