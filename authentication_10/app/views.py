from django.shortcuts import render
from .models import Chat, Group

# Create your views here.
def index(request, group_name):
    print('Group Name :', group_name)
    
    views_group = Group.objects.filter(name=group_name).first()
    
    chats = []
    if views_group:
        chats = Chat.objects.filter(model_group=views_group)
    else:
        group = Group(name=group_name)
        group.save()
    return render(request, 'app/index.html', {'groupname': group_name, 'chats': chats})
