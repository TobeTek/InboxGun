from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

from . import models 

# ViewSets define the view behavior.
class PostViewSet(viewsets.ModelViewSet):
    
    # Serializers define the API representation.
    class PostOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = models.Post
            fields = "__all__"

    queryset = models.Post.objects.all()
    serializer_class = PostOutputSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
