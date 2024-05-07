from django.urls import include , path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'apply', ApplyViewSet)
router.register(r'college', CollegeViewSet)
router.register(r'hire', HireViewSet)
router.register(r'jobapp', JobAppViewSet)
router.register(r'message', MessageViewSet)
router.register(r'post', PostViewSet)
router.register(r'student', StudentViewSet)
router.register(r'teacher', TeacherViewSet)
router.register(r'university', UniversityViewSet)
router.register(r'workin', WorkInViewSet)
router.register(r'users', UserViewSet)
router.register(r'skills', SkillViewSet)


urlpatterns = [
    # ahmed mostafa
    path('', include(router.urls)),
    path('login/', login, name='login'),
    path('university_applications/<int:university_id>/', university_applications, name='university_applications'),
    path('get_applicants/<int:university_id>/<int:application_id>', get_applicants, name='get_applicants'),
    path('delete_university_app/<int:university_id>/<int:application_id>', delete_university_app, name='delete_university_app'),
    path('get-user-by-username/<str:username>/', get_user_by_username, name='get_user_by_username'),
    path('university_views/<int:universityid>/<int:userid>/', university_views, name='university_views'),
    path('user_views/<int:visiting_user_id>/<int:visited_user_id>/', user_views, name='user_views'),
    path('users_who_visited_user/<int:user_id>/', users_who_visited_user, name='users_who_visited_user'),
    path('send_friend_request/<int:sender_id>/<int:receiver_id>', send_friend_request, name='send_friend_request'),
    path('get_waiting_list/<int:user_id>/', get_waiting_list, name='get_waiting_list'),
    path('add_skill_to_teacher/', add_skill_to_teacher, name='add-skill-to-teacher'),
    #######################################################################################
    # ali ayman 
    path('profile/<int:user_id>/', user_profile_api, name='user-profile'),
    path('user-info/', user_info_by_id_api, name='user-info-by-id'),
    path('remove-teacher-from-application/<int:university_id>/<int:app_id>/<int:teacher_id>/', remove_teacher_from_application_api, name='remove-teacher-from-application'),
    path('display-approved-teachers/<int:university_id>/<int:app_id>/', display_approved_teachers_in_specific_ap_api, name='display-approved-teachers'),
    path('get-profile-data/<int:user_id>/', get_profile_data_api, name='get-profile-data'),
    path('get-user-posts/<int:user_id>/', get_user_posts_api, name='get-user-posts'),
    path('posts/', get_all_posts_api, name='get_all_posts'),
    path('add-comment/', add_comment_api, name='add_comment'),
    path('delete-comment/<int:user_id>/<int:post_id>/<int:comment_id>/', delete_comment_api, name='delete_comment'),











    # token authentication
    path('api-auth/', include('rest_framework.urls')),
]