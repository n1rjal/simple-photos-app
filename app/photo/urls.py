from django.urls import path
from . import views


urlpatterns = [
    path(
        "<int:photo_id>/share/",
        views.SharePhotoAPIView.as_view(),
        name="share-photo",
    ),
    path(
        "<int:photo_id>/unshare/",
        views.UnsharePhotoAPIView.as_view(),
        name="unshare-photo",
    ),
    path(
        "<int:photo_id>/",
        views.PhotoViewset.as_view({"delete": "destroy"}),
        name="delete a photo",
    ),
    path(
        "",
        views.PhotoViewset.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="list photos",
    ),
]
