from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.Serializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_img = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):
        request = self.context['request']
        return request == obj.owner

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
            'id', 'owner', 'created_at', 'updated_at', 'title', 'content', 'image', 'is_owner', 'image_filter'
            ]