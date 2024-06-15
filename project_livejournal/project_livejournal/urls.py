from django.contrib import admin
from django.urls import path, include
from users import views as usersViews
from django.contrib.auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', usersViews.register, name='reg'),
    path('profile/', usersViews.profile, name='profile'),
    path('user/', authViews.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('', include('journal.urls')),
]
