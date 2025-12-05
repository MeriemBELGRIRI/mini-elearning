from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('<int:course_id>/edit/', views.course_update, name='course_update'),
    path('<int:course_id>/delete/', views.course_delete, name='course_delete'),
    path('<int:course_id>/lesson/create/', views.lesson_create, name='lesson_create'),
    # path('courses/<int:course_id>/lessons/add/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:pk>/edit/', views.lesson_update, name='lesson_update'),
    path('lessons/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),
]
