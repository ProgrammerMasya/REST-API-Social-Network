from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from home.models import Post

from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(methods=["get"], detail=False)
    def newest(self, request):
        newest = self.get_queryset().order_by("created").last()
        serializer = self.get_serializer_class()(newest)
        return Response(serializer.data)
