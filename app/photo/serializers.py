from django.contrib.auth.models import User
from rest_framework import serializers
from . import models


class PhotoMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhotoMetaData
        exclude = ["photo"]


class PhotoSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    metadata = PhotoMetaDataSerializer()
    access_users = serializers.StringRelatedField(many=True, read_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        metadata = validated_data.pop("metadata")

        photo = models.Photo.objects.create(owner=user, **validated_data)
        metadata = models.PhotoMetaData.objects.create(**metadata, photo=photo)

        return photo

    class Meta:
        model = models.Photo
        fields = "__all__"


# custom abstract user access serializers
# this will later be used for photo access and album access modifier


class UserPhotoAccessSerializer(serializers.Serializer):
    access_user_ids = serializers.ListSerializer(
        child=serializers.IntegerField(), write_only=True
    )

    def validate_user_ids(self, access_user_ids):
        # if user count is not equals to user_ids
        # we can say that some user is not found
        users_count = models.User.objects.filter(id__in=access_user_ids).count()
        if users_count != len(access_user_ids):
            raise serializers.ValidationError("Not all users are in the db")
        return access_user_ids

    def validate_photo_id(self, photo_id):
        photo_exists = models.Photo.objects.filter(id=photo_id).exists()
        if not photo_exists:
            raise serializers.ValidationError("Photo doesn't exist")
        return photo_exists

    def validate(self, attrs):
        photo_id = self.context["view"].kwargs.get("photo_id")
        self.validate_photo_id(photo_id)
        return attrs


class AddUserPhotoAccessSerializer(UserPhotoAccessSerializer):

    def create(self, validated_data):
        user_ids = validated_data.pop("access_user_ids")
        photo_id = self.context["view"].kwargs.get("photo_id")

        photo = models.Photo.objects.get(id=photo_id)
        users = User.objects.filter(id__in=user_ids)

        photo.access_users.add(*users)

        return photo


class RemoveUserPhotoAccessSerializer(UserPhotoAccessSerializer):

    def create(self, validated_data):
        user_ids = self.validated_data.pop("access_user_ids")
        photo_id = self.context["view"].kwargs.get("photo_id")

        photo = models.Photo.objects.get(id=photo_id)
        users = User.objects.filter(id__in=user_ids)

        photo.access_users.remove(*users)

        return photo
