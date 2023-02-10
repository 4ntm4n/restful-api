from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_img = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            liked = Like.objects.filter(
                owner=user, post=obj
            ).first()
            print(liked)
            return liked.pk if liked else None
        return None

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                "Image is larger than 2mb! upload a smaller image plz."
            )

        if value.image.width > 4096:
            raise serializers.ValidationError(
                "image width exeeds 4090px"
            )

        if value.image.height > 4096:
            raise serializers.ValidationError(
                "image height exeeds 4090px"
            )
        return value
            

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_img', 'created_at', 
            'updated_at', 'title', 'content', 'image', 'image_filter', 'like_id',
            'comments_count', 'likes_count'
            ]