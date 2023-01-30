from rest_framework import generics, permissions
from drf_api.permissions import isOwnerOrReadOnly
from .models import Follower
from .serializers import FollowerSerializer


class FollowersListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FollowerDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [isOwnerOrReadOnly]
    serializer_class = FollowerSerializer
    queryset = Follower.objects.all()
