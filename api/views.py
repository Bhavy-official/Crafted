from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Post, PostSection, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        post_type = self.request.query_params.get('post_type')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(tags__icontains=search)
            )

        if post_type:
            queryset = queryset.filter(post_type=post_type)

        return queryset

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['id']
        return Comment.objects.filter(post__id=post_id).order_by('created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['id']
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class PostLikeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        user = request.user
        like_obj, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            # already liked → unlike
            like_obj.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)


from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer

class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  

    def create(self, request, *args, **kwargs):
        
        data = request.data.dict()

        
        if 'sections' in data:
            import json
            try:
                data['sections'] = json.loads(data['sections'])
            except Exception as e:
                return Response({'error': 'Invalid sections JSON'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import os
from groq import Groq


client = Groq(api_key=os.environ.get("API_KEY"))


AI_BLOG_ID_COUNTER = 1

class AIGenerateBlogView(APIView):
   
    
    def post(self, request, *args, **kwargs):
        global AI_BLOG_ID_COUNTER

        topic = request.data.get("topic", "").strip()
        if not topic:
            return Response({"error": "Topic is required in the POST body."},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(topic) > 100:
            return Response({"error": "Topic too long (max 100 chars)."},
                            status=status.HTTP_400_BAD_REQUEST)

        prompt = (
            f"Write a detailed, well-structured blog post about '{topic}'. "
            "Include a short intro, 4-6 clear key points/subheadings with 2–4 sentences each, "
            "and a short conclusion. Keep tone professional and readable for developers."
        )

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful, professional blog writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200
            )

            blog_content = response.choices[0].message.content

            blog_data = {
                "id": AI_BLOG_ID_COUNTER,
                "title": f"AI Generated: {topic}",
                "description": f"AI generated article about {topic}",
                "content": blog_content,
                "author": "AI Assistant",
                "post_type": "ai-generated",
                "image": "/media/post_images/default.png",
                "tags": "ai,generated",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            AI_BLOG_ID_COUNTER += 1
            return Response(blog_data, status=status.HTTP_200_OK)

        except Exception as exc:
            return Response({"error": "AI generation failed", "detail": str(exc)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
