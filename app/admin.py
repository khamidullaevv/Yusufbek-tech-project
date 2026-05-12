from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, Balance, District, DistrictStudent, Teacher, 
    Group, Student, Payment, Expense, Homework, 
    News, Attendance, CustomSchedule
)

admin.site.site_header = _("EduSystem Management")
admin.site.site_title = _("EduSystem Admin Portal")
admin.site.index_title = _("Welcome to EduSystem Dashboard")

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('amount', 'last_updated')
    readonly_fields = ('last_updated',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')

@admin.register(DistrictStudent)
class DistrictStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'district', 'direction', 'status')
    list_filter = ('district', 'status', 'direction')
    search_fields = ('name', 'phone')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'phone', 'salary', 'status')
    list_filter = ('status', 'subject')
    search_fields = ('name', 'subject', 'phone')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id_code', 'subject', 'teacher', 'room', 'time', 'level')
    list_filter = ('level', 'teacher', 'room')
    search_fields = ('id_code', 'subject')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'group', 'paid', 'amount')
    list_filter = ('paid', 'group')
    search_fields = ('name', 'phone')
    list_editable = ('paid',) # Позволяет отмечать оплату прямо из списка

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'amount', 'month', 'date')
    list_filter = ('month', 'date')
    search_fields = ('student_name',)
    readonly_fields = ('date',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'paid')
    list_filter = ('paid',)
    search_fields = ('name',)

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'deadline')
    list_filter = ('group', 'deadline')
    search_fields = ('title',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('tag', 'text_preview', 'likes', 'date')
    readonly_fields = ('date',)

    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = _("Preview")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'date', 'status')
    list_filter = ('status', 'date', 'group')
    search_fields = ('student__name',)

@admin.register(CustomSchedule)
class CustomScheduleAdmin(admin.ModelAdmin):
    list_display = ('day', 'time', 'description')
    list_filter = ('day',)
    search_fields = ('description',)