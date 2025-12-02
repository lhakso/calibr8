from rest_framework import serializers
from .models import Prediction, UserProfile

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'description', 'probability', 'created_at', 'resolve_by', 'resolved', 'outcome']
        read_only_fields = ['id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'notes']
        read_only_fields = ['id']
