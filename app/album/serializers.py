from django.contrib.auth.models import User
from rest_framework import serializers

from photo.serializers import PhotoSerializer
from photo.models import Photo
from . import models


# made a class to contain shared code like mixin design in django
class UserAlbumAccessSerializer(serializers.Serializer):
    access_user_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), write_only=True
    )

    def validate_access_user_ids(self, user_ids):
        # if user count is not equals to user_ids
        # we can say that some user is not found
        users_count = models.User.objects.filter(id__in=user_ids).count()
        if users_count != len(user_ids):
            raise serializers.ValidationError("Not all users are in the db")
        return user_ids

    def validate_album_id(self, album_id):
        album_exists = models.Album.objects.filter(id=album_id).exists()
        if not album_exists:
            raise serializers.ValidationError("Album doesn't exist")
        return album_exists

    def validate(self, attrs):
        album_id = self.context["view"].kwargs.get("album_id")
        self.validate_album_id(album_id)
        return attrs


class AlbumPhotoSerializer(serializers.Serializer):
    photo_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), write_only=True
    )

    def validate_photo_ids(self, photo_ids):
        user = self.context["view"].request.user

        photos = Photo.objects.filter(
            id__in=photo_ids,
        )

        if photos.count() != len(photo_ids):
            raise serializers.ValidationError("Not all photos found")

        for photo in photos:
            if photo.owner != user:
                raise serializers.ValidationError("Photo doesn't belng to the user")

        return photo_ids

    def validate_album_id(self, album_id):
        user = self.context["view"].request.user
        album = models.Album.objects.filter(id=album_id).first()
        if not album:
            raise serializers.ValidationError("Album doesn't exist")
        if album.owner != user:
            raise serializers.ValidationError("Album doesn't belong to the user")
        return album_id

    def validate(self, attrs):
        album_id = self.context["view"].kwargs.get("album_id")
        self.validate_album_id(album_id)
        return attrs


class AlbumSerializer(serializers.ModelSerializer):
    access_users = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Album
        exclude = ["owner", "photos"]

    def create(self, validated_data):
        user = self.context["request"].user
        album = models.Album.objects.create(owner=user, **validated_data)
        return album


class ShareUserAlbumAccessSerializer(UserAlbumAccessSerializer):
    access_users = serializers.StringRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user_ids = validated_data.pop("access_user_ids")
        album_id = self.context["view"].kwargs.get("album_id")

        album = models.Album.objects.get(id=album_id)
        users = User.objects.filter(id__in=user_ids)

        album.access_users.add(*users)

        return album


class UnshareUserAlbumAccessSerializer(UserAlbumAccessSerializer):

    access_users = serializers.StringRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user_ids = validated_data.pop("access_user_ids")
        album_id = self.context["view"].kwargs.get("album_id")

        album = models.Album.objects.get(id=album_id)
        users = User.objects.filter(id__in=user_ids)

        album.access_users.remove(*users)

        return album


class SharePhotoInAlbumSerializer(AlbumPhotoSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    def create(self, validated_data):
        photo_ids = validated_data.pop("photo_ids")
        album_id = self.context["view"].kwargs.get("album_id")

        album = models.Album.objects.get(id=album_id)
        photos = Photo.objects.filter(id__in=photo_ids)

        album.photos.add(*photos)

        return album


class UnsharePhotoInAlbumSerializer(AlbumPhotoSerializer):
    photos = PhotoSerializer(many=True, read_only=True)

    def save(self, validated_data):
        photo_ids = validated_data.pop("photo_ids")
        album_id = self.context["view"].kwargs.get("album_id")

        album = models.Album.objects.get(id=album_id)
        photos = Photo.objects.filter(id__in=photo_ids)

        album.photos.remove(*photos)

        return album
