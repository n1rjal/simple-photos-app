from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from . import models
from . import serializers
from . import filters

# Create your views here.


class PhotoViewset(viewsets.ModelViewSet):
    serializer_class = serializers.PhotoSerializer
    queryset = models.Photo.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.PhotoFilter

    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        context.update(
            {
                "photo_id": kwargs.get("photo_id"),
                "request": self.request,
            }
        )
        return context


class SharePhotoAPIView(generics.CreateAPIView):
    serializer_class = serializers.AddUserPhotoAccessSerializer


class UnsharePhotoAPIView(generics.CreateAPIView):
    serializer_class = serializers.RemoveUserPhotoAccessSerializer
