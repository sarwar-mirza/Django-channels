from django.contrib import admin
from .models import Group, Chat

# Register your models here.
@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'timeStamp', 'model_group']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']




