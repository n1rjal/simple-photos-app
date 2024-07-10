from drf_yasg.utils import swagger_auto_schema
from . import serializers
from . import models
from rest_framework import viewsets, generics

# Create your views here.


class AlbumViewset(viewsets.ModelViewSet):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
    lookup_url_kwarg = "album_id"
    lookup_field = "id"

    def get_queryset(self):
        return models.Album.objects.filter(owner__username="testuser").order_by(
            "-created_at"
        )

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class ShareAlbumAPIView(generics.CreateAPIView):
    serializer_class = serializers.ShareUserAlbumAccessSerializer


class UnshareAlbumAPIView(generics.CreateAPIView):
    serializer_class = serializers.UnshareUserAlbumAccessSerializer


class SharePhotoInAlbumAPIView(generics.CreateAPIView):
    serializer_class = serializers.SharePhotoInAlbumSerializer


class UnsharePhotoInAlbumAPIView(generics.CreateAPIView):
    serializer_class = serializers.UnshareUserAlbumAccessSerializer
