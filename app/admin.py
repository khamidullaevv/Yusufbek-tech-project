from django.contrib import admin
from .models import User, Group, Attendance, Payment, Post

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'phone')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    search_fields = ('name',)   

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'date', 'is_present')
    list_filter = ('is_present', 'date')
    search_fields = ('student__username', 'group__name')
    
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'date_paid')
    search_fields = ('student__username',)  
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
