from rest_framework import routers

from home.api.viewsets import PostViewSet

router = routers.DefaultRouter()
router.register("posts", PostViewSet, base_name="post")
