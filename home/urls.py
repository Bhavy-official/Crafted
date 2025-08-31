from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('write', views.write, name='write'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('ai-generate/', views.ai_generate, name='ai-generate'),
    path('post/<int:post_id>/', views.post_detail, name='post-detail'),
]
