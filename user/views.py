from rest_framework import viewsets, views, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import detail_route


from .models import *
from .serializers import *
from .permissions import *

# Create your views here.


class PostView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminCreate,)

    @action(methods=['post'], detail=False, permission_classes=[AllowAny])
    def create_user(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class LikeView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner, )
    queryset = UserLike.objects.all()
    serializer_class = LikeSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.queryset.none()
        elif self.request.user.is_superuser:
            return self.queryset
        else:
            return self.request.user.likes.all()

    def destroy(self, request, pk=None):
        like = get_object_or_404(self.queryset, pk=pk)
        like.active = False
        like.save()
        return Response({'result': 'cant delete like'}, status=status.HTTP_400_BAD_REQUEST)
