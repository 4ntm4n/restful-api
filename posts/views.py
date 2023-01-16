from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import isOwnerOrReadOnly


class PostListView(APIView):
    """
    get all post objects
    serialize posts query

    """
    # set serializer class to render a form
    serializer_class = PostSerializer
    # set permissions array containing permission classes.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

class PostDetailView(APIView):
    #set serializer class to render a 'post' form
    serializer_class = PostSerializer
    #set permission array containing built in django permission classes
    permission_classes = [isOwnerOrReadOnly]
    
    def get_object(self, pk):
        """
        try to get a specific post by id 
        return 404 error if post not found
        """
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except:
            raise Http404

    def get(self, request, pk):
        """
        1. if post exist, get post object
        2. serialize it
        3. return serialized data to the view specified in urls.py
        """
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        method for updating a post.
        1. get post object by id
        2. serialize object for the view
        3. create logic to save serialized data if data is valid
        else return a 404 BAD REQUEST error message.
        """

        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        this method makes it posible to delete a post
        from within the detail view.
        """
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
