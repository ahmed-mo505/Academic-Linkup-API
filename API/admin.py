
from django.contrib import admin
from .models import University, Student, Teacher, User,Post,Comment,JobApp

# Register your models here.

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['user','id','name', 'logo', 'about']
    # search_fields = ['university_name', 'university_email']

# @admin.register(Student)
# class StudentAdmin(admin.ModelAdmin):
#     list_display = ['student_id', 'student_name', 'student_degree', 'university', 'college']
#     search_fields = ['student_name', 'student_degree']
#     list_filter = ['university']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

# The model User is already registered with 'auth.UserAdmin'
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ['id', 'username', 'email']
#     search_fields = ['username', 'email']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'post_text', 'time_stamp', 'teacher', 'university', 'student']
    search_fields = ['post_id', 'post_text', 'teacher__name', 'university__name', 'student__name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'body', 'created_by', 'created_at']
    search_fields = ['body', 'created_by__username']  # Search by body and username
    list_filter = ['created_at']  # Filter by created_at date    



@admin.register(JobApp)
class JobAppAdmin(admin.ModelAdmin):
    list_display = ['department', 'location', 'deadline', 'university']
    search_fields = ['department', 'location', 'university__name']
    list_filter = ['deadline', 'university']    