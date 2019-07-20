from django.contrib import admin
from .models import Photo
# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
    list_display=('author', 'text', 'created_at')

admin.site.register(Photo,PhotoAdmin)
