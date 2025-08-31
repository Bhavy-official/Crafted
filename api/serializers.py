from rest_framework import serializers
from .models import CustomUser, Post, PostSection, Like, Comment


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'bio', 'profile_pic']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_pic=validated_data.get('profile_pic', None),
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'user_name', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


from rest_framework import serializers
from .models import Post, PostSection, Comment, Like

class PostSectionSerializer(serializers.ModelSerializer):
    section_title = serializers.CharField(source='title')
    section_content = serializers.CharField(source='description')

    class Meta:
        model = PostSection
        fields = ['order', 'section_title', 'section_content']

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    sections = PostSectionSerializer(many=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField() 
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'description', 'author', 'author_name', 'post_type',
            'image', 'tags', 'created_at', 'updated_at', 'sections',
            'likes_count', 'comments_count', 'comments' 
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count() 
    def get_comments_count(self, obj):
        count = obj.comments.count()
        print(f"Post {obj.id} has {count} comments")
        return count

    def create(self, validated_data):
        sections_data = validated_data.pop('sections', [])
        post = Post.objects.create(**validated_data)

        for index, section in enumerate(sections_data):
            PostSection.objects.create(
                post=post,
                title=section['title'],
                description=section['description'],
                order=section.get('order', index)
            )
        return post

    def update(self, instance, validated_data):
        sections_data = validated_data.pop('sections', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if sections_data is not None:
            instance.sections.all().delete()
            for index, section in enumerate(sections_data):
                PostSection.objects.create(
                    post=instance,
                    title=section['title'],
                    description=section['description'],
                    order=section.get('order', index)
                )
        return instance

