
# Create your views here.

from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated ,AllowAny,IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404



class ApplyViewSet(viewsets.ModelViewSet):
    queryset = Apply.objects.all()
    serializer_class = ApplySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class HireViewSet(viewsets.ModelViewSet):
    queryset = Hire.objects.all()
    serializer_class = HireSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class JobAppViewSet(viewsets.ModelViewSet):
    queryset = JobApp.objects.all()
    serializer_class = JobAppSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        student_data = request.data.get('student', {})

        # Hash the password before saving the user
        user_data['password'] = make_password(user_data.get('password'))
        
        # First, create the User object
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Associate the user with the student and create the student object
        student_data['user'] = user.id
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student_serializer.save()
            return Response(student_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Rollback user creation if student creation fails
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        teacher_data = request.data.get('teacher', {})

        # Hash the password before saving the user
        user_data['password'] = make_password(user_data.get('password'))
        
        # First, create the User object
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Associate the user with the teacher and create the teacher object
        teacher_data['user'] = user.id
        teacher_serializer = TeacherSerializer(data=teacher_data)
        if teacher_serializer.is_valid():
            teacher_serializer.save()
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Rollback user creation if teacher creation fails
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        university_data = request.data.get('university', {})

        # Hash the password before saving the user
        user_data['password'] = make_password(user_data.get('password'))
        
        # First, create the User object
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Associate the user with the university and create the university object
        university_data['user'] = user.id
        university_serializer = UniversitySerializer(data=university_data)
        if university_serializer.is_valid():
            university_serializer.save()
            return Response(university_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Rollback user creation if university creation fails
            return Response(university_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WorkInViewSet(viewsets.ModelViewSet):
    queryset = WorkIn.objects.all()
    serializer_class = WorkInSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

# user login
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'message': 'Login successful','token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def university_applications(request, university_id):
    try:
        university = University.objects.get(id=university_id)
        applications = JobApp.objects.filter(university=university)
        serializer = JobAppSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except University.DoesNotExist:
        return Response({"error": "University not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_applicants(request, university_id, application_id):
    try:
        # Retrieve all Apply instances for the given university and application IDs
        applicants = Apply.objects.filter(university=university_id, application=application_id)
        
        # Serialize the applicants data
        serializer = ApplySerializer(applicants, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Apply.DoesNotExist:
        return Response({"error": "No applicants found for the specified job application and university"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_university_app(request, university_id, application_id):
    try:
        # Check if the job application exists for the given university and application IDs
        job_app = JobApp.objects.get(university_id=university_id, id=application_id)
        
        # Delete the job application
        job_app.delete()
        
        return Response({"message": "Job application deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except JobApp.DoesNotExist:
        return Response({"error": "Job application not found for the specified university and application IDs"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_by_username(request, username):
    if request.method == 'GET':
        if username is not None:
            try:
                user = User.objects.get(username=username)
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
                try:
                    student = Student.objects.get(user=user)
                    user_data['student_data'] = {
                        'student_id': student.id,
                        'name': student.name,
                        'title': student.title,
                        # 'user_bg_img': student.user_bg_img,
                        # 'user_img': student.user_img,
                        # Add other fields from Student model
                    }
                except Student.DoesNotExist:
                    pass  # No student data found for this user

                try:
                    teacher = Teacher.objects.get(user=user)
                    user_data['teacher_data'] = {
                        'teacher_id': teacher.id,
                        'name': teacher.name,
                        # 'user_img': teacher.user_img,
                        # 'user_bg_img': teacher.user_bg_img,
                        'title': teacher.title,
                        # Add other fields from Teacher model
                    }
                except Teacher.DoesNotExist:
                    pass  # No teacher data found for this user

                try:
                    university = University.objects.get(user=user)
                    user_data['university_data'] = {
                        'university_id': university.id,
                        'name': university.name,
                        'about': university.about,
                        # 'logo': university.logo,
                        # 'university_bg_img': university.university_bg_img,
                        # Add other fields from University model
                    }
                except University.DoesNotExist:
                    pass  # No university data found for this user

                return Response(user_data, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Username parameter is missing'}, status=status.HTTP_400_BAD_REQUEST)        

# same as user_views
@api_view(['POST'])
def university_views(request, universityid, userid):
    university = get_object_or_404(University, id=universityid)
    user = get_object_or_404(User, id=userid)

    # Add the user to recent visits
    university.recent_visits.add(user)  

    # Increment profile_views for the university
    university.profile_views += 1
    university.save()

    return Response({'success': 'University views incremented successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def user_views(request, visiting_user_id, visited_user_id):
    visiting_user = get_object_or_404(User, id=visiting_user_id)
    visited_user = get_object_or_404(User, id=visited_user_id)

    if Student.objects.filter(user_id=visited_user_id).exists():
        visited_student = get_object_or_404(Student, user_id=visited_user_id)
        visited_student.recent_visits.add(visiting_user)
        visited_student.profile_views += 1
        visited_student.save()
        return Response({'success': 'Student profile views incremented successfully'}, status=status.HTTP_200_OK)
    elif Teacher.objects.filter(user_id=visited_user_id).exists():
        visited_teacher = get_object_or_404(Teacher, user_id=visited_user_id)
        visited_teacher.recent_visits.add(visiting_user)
        visited_teacher.profile_views += 1
        visited_teacher.save()
        return Response({'success': 'Teacher profile views incremented successfully'}, status=status.HTTP_200_OK)
    elif University.objects.filter(user_id=visited_user_id).exists():
        visited_university = get_object_or_404(University, user_id=visited_user_id)
        visited_university.recent_visits.add(visiting_user)
        visited_university.profile_views += 1
        visited_university.save()
        return Response({'success': 'University profile views incremented successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User type not recognized'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def users_who_visited_user(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)

        # Check if the user is a teacher
        if Teacher.objects.filter(user_id=user_id).exists():
            teacher = get_object_or_404(Teacher, user_id=user_id)
            visitors = teacher.recent_visits.all()

        # Check if the user is a university
        elif University.objects.filter(user_id=user_id).exists():
            university = get_object_or_404(University, user_id=user_id)
            visitors = university.recent_visits.all()

        # Check if the user is a student
        elif Student.objects.filter(user_id=user_id).exists():
            student = get_object_or_404(Student, user_id=user_id)
            visitors = student.recent_visits.all()

        # If the user is not a teacher, university, or student, return an error
        else:
            return Response({'error': 'User is not a teacher, university, or student'}, status=status.HTTP_400_BAD_REQUEST)

        visitor_data = [{'id': visitor.id, 'username': visitor.username} for visitor in visitors]

        return Response({'visitors': visitor_data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def send_friend_request(request, sender_id, receiver_id):
    try:
        sender = get_object_or_404(User, id=sender_id)
        receiver = get_object_or_404(User, id=receiver_id)

        # Check if receiver is a teacher
        if Teacher.objects.filter(user_id=receiver_id).exists():
            receiver_teacher = get_object_or_404(Teacher, user_id=receiver_id)
            receiver_teacher.friend_requests.add(sender_id)
            receiver_teacher.save()
            return Response({'success': 'Friend request sent successfully'}, status=status.HTTP_200_OK)
        # Check if receiver is a student
        elif Student.objects.filter(user_id=receiver_id).exists():
            receiver_student = get_object_or_404(Student, user_id=receiver_id)
            receiver_student.friend_requests.add(sender_id)
            receiver_student.save()
            return Response({'success': 'Friend request sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Sender is neither a teacher nor a student'}, status=status.HTTP_400_BAD_REQUEST)
        
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_waiting_list(request, user_id):
    try:
        # Check if the user is a teacher
        if Teacher.objects.filter(user_id=user_id).exists():
            teacher = Teacher.objects.get(user_id=user_id)
            friend_list = teacher.friends.all()
        # Check if the user is a student
        elif Student.objects.filter(user_id=user_id).exists():
            student = Student.objects.get(user_id=user_id)
            friend_list = student.friends_list.all()
        else:
            return Response({'error': 'User not found or not a teacher/student'}, status=status.HTTP_404_NOT_FOUND)

        # response data
        friend_data = [{'id': friend.id, 'username': friend.username} for friend in friend_list]

        return Response({'waiting_list': friend_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_skill_to_teacher(request, skill_id, teacher_id):
    if request.method == 'POST':
        try:
            teacher = Teacher.objects.get(pk=teacher_id)
            skill = Skill.objects.get(pk=skill_id)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher with specified ID does not exist."}, status=404)
        except Skill.DoesNotExist:
            return Response({"error": "Skill with specified ID does not exist."}, status=404)

        teacher.skills.add(skill)
        return Response({"success": "Skill added to teacher successfully."}, status=200)
    else:
        return Response({"error": "Only POST method is allowed."}, status=405)


#************************************************************************

@api_view(['GET'])
def user_profile_api(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        univ = University.objects.get(user_id=user.id)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
    except University.DoesNotExist:
        return Response({"error": "University does not exist for this user"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UniversitySerializer(univ)
    return Response(serializer.data)

@api_view(['GET'])
def user_info_by_id_api(request):
    user_ids = request.query_params.get('ids', '')  # Get the value of 'ids' parameter from the query params
    user_ids = user_ids.split(',')  # Split the string into a list using comma as delimiter
    users = []

    for user_id in user_ids:
        try:
            user = None
            if user_id.isdigit():  # Check if the user_id is a valid integer
                user_id = int(user_id)
                student = Student.objects.filter(pk=user_id).first()  # Try to get a student with the given ID
                if student:
                    users.append((student, 'student'))
                else:
                    university = University.objects.filter(pk=user_id).first()  # Try to get a university with the given ID
                    if university:
                        users.append((university, 'university'))
                    else:
                        teacher = Teacher.objects.filter(pk=user_id).first()  # Try to get a teacher with the given ID
                        if teacher:
                            users.append((teacher, 'teacher'))
            else:
                # Handle the case when the user_id is not a valid integer
                # You can choose to return an error response or handle it as needed
                pass
        except Exception as e:
            # Handle any exceptions that occur during the retrieval process
            pass

    serialized_users = []
    for user, user_type in users:
        if user_type == 'student':
            serializer = StudentSerializer(user)
        elif user_type == 'university':
            serializer = UniversitySerializer(user)
        elif user_type == 'teacher':
            serializer = TeacherSerializer(user)
        serialized_users.append(serializer.data)
    
    return Response(serialized_users, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def remove_teacher_from_application_api(request, university_id, app_id, teacher_id):
    try:
        # Check if all required parameters are provided
        if university_id is None or app_id is None or teacher_id is None:
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the objects exist
        university = University.objects.get(pk=university_id)
        application = JobApp.objects.get(pk=app_id)
        teacher = Teacher.objects.get(pk=teacher_id)

        # Remove the teacher from the application
        application.teachers.remove(teacher)

        return Response({'message': 'Teacher removed from application successfully'}, status=status.HTTP_200_OK)
    except (University.DoesNotExist, JobApp.DoesNotExist, Teacher.DoesNotExist):
        return Response({'error': 'Invalid university_id, app_id, or teacher_id'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def display_approved_teachers_in_specific_ap_api(request, university_id, app_id):
    try:
        # Retrieve the university object
        university = University.objects.get(pk=university_id)

        # Retrieve the application object for the specified university
        application = JobApp.objects.get(pk=app_id, university=university)

        # Get the approved teachers for the application
        approved_teachers = application.teachers.filter(approved=True)

        # Serialize the approved teachers data
        serialized_teachers = [teacher.serialize() for teacher in approved_teachers]

        return Response(serialized_teachers, status=status.HTTP_200_OK)
    except (University.DoesNotExist, JobApp.DoesNotExist):
        return Response({'error': 'Invalid university_id or app_id'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_profile_data_api(request, user_id):
    try:
        # Check if user is a university
        university = University.objects.filter(user_id=user_id).first()
        if university:
            data = {
                'name': university.name,
                'img': university.logo.url if university.logo else None,
                'bg_img': university.university_bg_img.url if university.university_bg_img else None,
                'title': university.rule,
                'about': university.about
            }
            return Response(data, status=status.HTTP_200_OK)

        # Check if user is a student
        student = Student.objects.filter(user_id=user_id).first()
        if student:
            data = {
                'name': student.user.username,
                'img': student.user_img.url if student.user_img else None,
                'bg_img': None,
                'title': student.title,
                'about': student.about
            }
            return Response(data, status=status.HTTP_200_OK)

        # Check if user is a teacher
        teacher = Teacher.objects.filter(user_id=user_id).first()
        if teacher:
            data = {
                'name': teacher.user.username,
                'img': teacher.user_img.url if teacher.user_img else None,
                'bg_img': None,
                'title': teacher.title,
                'about': teacher.about
            }
            return Response(data, status=status.HTTP_200_OK)

        # User with the given ID is not found
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_user_posts_api(request, user_id):
    try:
        # Determine the user type based on the context of the request
        # For example, if the URL pattern indicates the user type
        if 'teacher' in request.path:
            user_posts = Post.objects.filter(teacher_id=user_id)
        elif 'student' in request.path:
            user_posts = Post.objects.filter(student_id=user_id)
        elif 'university' in request.path:
            user_posts = Post.objects.filter(university_id=user_id)
        else:
            return Response({'error': 'Unable to determine user type'}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the posts data using PostSerializer
        serializer = PostSerializer(user_posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_posts_api(request):
    try:
        # Retrieve all posts
        all_posts = Post.objects.all()

        # Serialize the posts data using PostSerializer
        serializer = PostSerializer(all_posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def add_comment_api(request):
    try:
        # Extract user_id, post_id, and comment from query parameters
        user_id = request.query_params.get('user_id')
        post_id = request.query_params.get('post_id')
        comment_text = request.query_params.get('comment')

        # Validate user_id, post_id, and comment
        if not user_id or not post_id or not comment_text:
            return Response({'error': 'User ID, Post ID, and Comment are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the post
        post = Post.objects.get(pk=post_id)

        # Create the comment
        comment = Comment.objects.create(user_id=user_id, post=post, text=comment_text)

        # Serialize the comment data
        serializer = CommentSerializer(comment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Post.DoesNotExist:
        return Response({'error': 'Post does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

@api_view(['DELETE'])
def delete_comment_api(request, user_id, post_id, comment_id):
    try:
        # Check if the comment exists
        comment = Comment.objects.get(pk=comment_id, post_id=post_id)

        # Check if the user is authorized to delete the comment (optional)
        if comment.user_id != user_id:
            return Response({'error': 'You are not authorized to delete this comment'}, status=status.HTTP_403_FORBIDDEN)

        # Delete the comment
        comment.delete()

        return Response({'message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment does not exist'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)