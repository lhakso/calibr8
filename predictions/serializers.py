from rest_framework import serializers
from .models import Prediction, UserProfile
from django.utils import timezone

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ['id', 'description', 'probability', 'created_at', 'resolve_by', 'resolved', 'outcome']
        read_only_fields = ['id', 'created_at']

    def validate_description(self, value):
        """Validate prediction description"""
        if not value or not value.strip():
            raise serializers.ValidationError("Description cannot be empty")
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters")
        if len(value) > 500:
            raise serializers.ValidationError("Description cannot exceed 500 characters")
        return value.strip()

    def validate_probability(self, value):
        """Validate probability is between 0.0 and 1.0"""
        if value < 0.0 or value > 1.0:
            raise serializers.ValidationError("Probability must be between 0.0 and 1.0")
        return value

    def validate_resolve_by(self, value):
        """Validate resolve_by date is in the future"""
        if value and value < timezone.now():
            raise serializers.ValidationError("Resolve date must be in the future")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'notes']
        read_only_fields = ['id']
