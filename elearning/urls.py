from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('', RedirectView.as_view(url='/users/login/', permanent=False)),
]