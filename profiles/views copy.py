from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import isOwnerOrReadOnly

class ProfileListView(APIView):
    """ 
    get all profiles,
    serialice profiles
    return serialized data to the url specified in urls.py
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileDetailView(APIView):
    # set serializer class to render a form
    serializer_class = ProfileSerializer
    # set permissions array containing permission classes.
    permission_classes = [isOwnerOrReadOnly]

    def get_object(self, pk):
        """
        try to get the oject for a specific profile
        using it's id.

        return 404 if id not found
        """
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except:
            raise Http404
    
    def get(self, request, pk):
        """
        if profile exists, get profile object
        serialize it
        return serialized data to the specified url in urls.py
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(
            profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)