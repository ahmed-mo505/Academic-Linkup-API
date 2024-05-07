import uuid
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils.timesince import timesince



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # student_id = models.CharField(max_length=20, primary_key=True)
    # Add other student-related fields here
    name = models.CharField(max_length=255,null=True)
    user_img = models.ImageField(upload_to="student_img",null=True)
    user_bg_img = models.ImageField(upload_to="student_img",null=True)
    title = models.CharField(max_length=255,null=True)
    about = models.TextField(max_length=255,null=True)
    friend_list = models.ManyToManyField(User, symmetrical=False, related_name="friends_list",blank=True)
    friend_requests = models.ManyToManyField(User, symmetrical=False, related_name="friend_requests",blank=True)

    # degree = models.CharField(max_length=255,blank=True,null=True)
    # Gender = models.CharField(max_length=255,blank=True,null=True)
    # # enrolls : one university with many students
    # university = models.ForeignKey(University,blank=True, null=True)
    # # study_in : one college with many students
    # college = models.ForeignKey(College,blank=True, null=True)
    # poster_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    # message_id = models.ForeignKey(Message,on_delete=models.CASCADE,blank=True,null=True)
    # college_id = models.ForeignKey(College,blank=True,null=True)


    def __str__(self):
        return self.user.username  # Or any other field you want to represent

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Skill(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # teacher_id = models.CharField(max_length=20, primary_key=True)
    # Add other teacher-related fields here
    rule = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    qualitative = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    user_img = models.ImageField(upload_to="teacher_img",null=True)
    user_bg_img = models.ImageField(upload_to="teacher_img",null=True)
    title = models.CharField(max_length=255,null=True)
    about = models.TextField(max_length=255,null=True)
    friend_list = models.ManyToManyField(User, symmetrical=False, related_name="friends",blank=True)
    friend_requests = models.ManyToManyField(User, symmetrical=False, related_name="pending_friend_requests",blank=True)
    post_views = models.IntegerField(default=0, null=True, blank=True)  
    profile_views = models.IntegerField(default=0, null=True, blank=True)
    recent_visits = models.ManyToManyField(User, symmetrical=False, related_name='recently_visited_by_user', blank=True)
    skills = models.ManyToManyField(Skill, related_name='teachers_skills', blank=True)

    def __str__(self):
        return self.user.username  # Or any other field you want to represent

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    is_accepted = models.BooleanField(default=False)

class University(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # university_id = models.CharField(max_length=20, primary_key=True)
    # Add other university-related fields here
    rule = models.CharField(max_length=255,null=True)
    name = models.CharField(max_length=255,null=True)
    logo = models.ImageField(upload_to="university_img",null=True)
    university_bg_img = models.ImageField(upload_to="university_img",null=True)
    about = models.TextField(max_length=1000,null=True)
    post_views = models.IntegerField(default=0, help_text="Number of post views for the university")
    profile_views = models.IntegerField(default=0, help_text="Number of profile views for the university")
    recent_visits = models.ManyToManyField(User, symmetrical=False, related_name='recently_visited_by', blank=True)
    followers_list = models.ManyToManyField(User, symmetrical=False, related_name='followers', blank=True)
    followe_requests = models.ManyToManyField(User, symmetrical=False, related_name="pending_follow_requests",blank=True)
    university_auth_file = models.FileField(upload_to="university_files", null=True, blank=True)

    def __str__(self):
        return self.user.username  # Or any other field you want to represent

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"

class FollowRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_follow_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_follow_requests')
    is_accepted = models.BooleanField(default=False)        

class College(models.Model):
    # college_id = models.CharField(max_length=20, primary_key=True)
    college_name = models.CharField(max_length=255)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    def __str__(self):
        return self.college_name

    class Meta:
        verbose_name = "College"
        verbose_name_plural = "Colleges"

class JobApp(models.Model):
    # application_id = models.CharField(max_length=20, primary_key=True)
    department = models.CharField(max_length=255,blank=True, null=True)
    location = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE)

    skills_required = models.ManyToManyField(Skill, related_name='jobapp_required_skills', blank=True)
    qualitative_required = models.CharField(max_length=100, blank=True, null=True)
    subject_required = models.CharField(max_length=100, blank=True, null=True)
    experience_required = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        # return f"Application ID: {self.application_id}"
        return f"{self.description} at {self.university.name}"

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"

class Apply(models.Model):
    application = models.ForeignKey(JobApp, on_delete=models.CASCADE,null=True,blank=True)
    user_apply = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f"Application: {self.application} - User: {self.user_apply.username}"

    class Meta:
        verbose_name = "Job Apply"
        verbose_name_plural = "Job Applies"
        unique_together = (('application', 'user_apply'),)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_at',)
    
    def created_at_formatted(self):
        return timesince(self.created_at)

class Post(models.Model):
    post_id = models.CharField(max_length=20, primary_key=True)
    post_text = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='post_img/%Y/%m/%d', blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Post {self.post_id}"

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Message(models.Model):
    # message_id = models.CharField(max_length=20,primary_key=True)
    content = models.TextField(blank=True, null=True)
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sent_messages', blank=True, null=True)
    receiver = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='received_messages', blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE,related_name='related_messages', blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='related_messages', blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='related_messages', blank=True, null=True)

    def __str__(self):
        return f"Message {self.message_id}"  # Customize the representation as needed

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

class WorkIn(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, primary_key=True)
    collage = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return f"WorkIn {self.teacher}"  # Customize the representation as needed

    class Meta:
        verbose_name = "WorkIn"
        verbose_name_plural = "WorkIns"
        unique_together = (('teacher', 'collage'),)

class Hire(models.Model):
    university = models.OneToOneField(University, on_delete=models.CASCADE, primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f"Hire: {self.university}, {self.teacher}"  # Customize the representation as needed

    class Meta:
        verbose_name = "Hire"
        verbose_name_plural = "Hires"
        unique_together = (('university', 'teacher'),)

# signals
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def TokenCreate(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)