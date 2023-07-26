from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.registrationpg),
    path('reg-data/',views.RegistrationApi.as_view(),name='reg-data'),
    path('login/',views.login),
    path('login-data/',views.LoginAPi.as_view(),name='login-data'),
    path('upload-file/',views.upload_files),
    path('upload-files-data/',views.upload_files_data),
    path('download/<int:id>/',views.download),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
