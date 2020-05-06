from rest_framework import serializers
from django.contrib.auth.models import User
from .models import like_model,favorite_model,channel_model

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = like_model
        fields = ('user', 'part_id')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = favorite_model
        fields = ('user', 'part_id')

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = channel_model
        fields = ('user', 'username')
