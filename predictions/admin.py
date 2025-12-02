from django.contrib import admin
from .models import Prediction, UserProfile

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['description', 'probability', 'resolved', 'outcome', 'created_at']
    list_filter = ['resolved', 'outcome']
    search_fields = ['description']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['name']
