from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.models import User

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_verified')  
    search_fields = ('user__username', 'user__email')  # Add search fields
    list_filter = ('email_verified',)  
