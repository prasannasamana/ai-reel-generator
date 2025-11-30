from django.contrib import admin
from .models import ReelJob


@admin.register(ReelJob)
class ReelJobAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_at', 'tone']
    list_filter = ['status', 'tone', 'created_at']
    search_fields = ['id', 'original_script']
    readonly_fields = ['id', 'created_at', 'updated_at']

