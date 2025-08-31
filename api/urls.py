from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView , TokenBlacklistView 
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('posts/', views.PostListAPIView.as_view(), name='post-list'),
    path('posts/<int:id>/', views.PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:id>/comments/', views.CommentListCreateAPIView.as_view(), name='post-comments'),
    path('posts/<int:id>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    path('posts/create/', views.PostCreateAPIView.as_view(), name='post-create'),

    path('posts/ai-generate/', views.AIGenerateBlogView.as_view(), name='ai-generate'),

]

