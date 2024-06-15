from django.contrib import admin
from django.urls import path, include
from users import views as usersViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reg', usersViews.register, name='reg'),
    path('', include('journal.urls')),
]
