from django.http import Http404
from rest_framework import generics, permissions
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import isOwnerOrReadOnly


class PostListView(generics.ListCreateAPIView):
    """
    get all post objects
    serialize posts query

    """
    # set serializer class to render a form
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [isOwnerOrReadOnly]
    queryset = Post.objects.all()
