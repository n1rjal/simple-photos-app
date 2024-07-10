from django_filters import rest_framework as filters

from photo.models import Photo


class PhotoFilter(filters.FilterSet):
    album_id = filters.NumberFilter(method="filter_by_album_id")

    def filter_by_album_id(self, queryset, name, value):
        if value:
            queryset = queryset.filter(albums__id=value)
        queryset = queryset.order_by("-metadata__capture_time")
        return queryset

    class Meta:
        model = Photo
        fields = ["album_id"]
