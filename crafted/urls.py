from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create superuser view
def create_superuser(request):
    # Get superuser details from environment variables
    superuser_name = os.getenv('SUPERUSER_USERNAME', 'admin')
    superuser_email = os.getenv('SUPERUSER_EMAIL', 'admin@example.com')
    superuser_password = os.getenv('SUPERUSER_PASSWORD', 'yourpassword')

    # Check if superuser already exists
    if not User.objects.filter(username=superuser_name).exists():
        User.objects.create_superuser(superuser_name, superuser_email, superuser_password)
        return HttpResponse(f"Superuser {superuser_name} created successfully!")
    return HttpResponse(f"Superuser {superuser_name} already exists.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('api/', include('api.urls')),  # main API
    path('create_superuser/', create_superuser),  # Temporary URL for creating superuser
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
