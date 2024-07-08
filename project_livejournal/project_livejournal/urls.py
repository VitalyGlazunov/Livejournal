from django.contrib import admin
from django.urls import path, include
from users.views import RegisterView, ProfileSettingsView, ProfileView
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg/', RegisterView.as_view(), name='reg'),
    path('profile-settings', ProfileSettingsView.as_view(), name='profile_settings'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user/', authViews.LoginView.as_view(template_name='users/user.html'), name='user'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('', include('journal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)