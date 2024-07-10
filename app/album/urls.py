from django.urls import path
from .routers import urlpatterns
from . import views

urlpatterns = [
    path(
        "<int:album_id>/users/share/",
        views.ShareAlbumAPIView.as_view(),
        name="share-album-view",
    ),
    path(
        "<int:album_id>/users/unshare/",
        views.UnshareAlbumAPIView.as_view(),
        name="unshare-album-view",
    ),
    path(
        "<int:album_id>/photos/share/",
        views.SharePhotoInAlbumAPIView.as_view(),
        name="add-photo-view",
    ),
    path(
        "<int:album_id>/photos/unshare/",
        views.UnsharePhotoInAlbumAPIView.as_view(),
        name="add-photo-view",
    ),
] + urlpatterns
