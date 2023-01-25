from rest_framework import generics, permissions
from drf_api.permissions import isOwnerOrReadOnly
from .models import Like
from .serializers import LikeSerializer

class LikeListView(generics.ListCreateAPIView):
    """
    List likes or create a like if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LikeDetailView(generics.RetrieveDestroyAPIView):
    permission_classes =[isOwnerOrReadOnly]
    serializer_class = LikeSerializer
    queryset = Like.objects.all()