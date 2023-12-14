from django.shortcuts import render
from .models import Chat, Group

# Ex-02(real time)
def index(request, group_name):
    print('Group Name :', group_name)
    
    views_GroupName = Group.objects.filter(name=group_name).first()
    
    chats = []
    if views_GroupName:
        chats = Chat.objects.filter(model_group=views_GroupName)
    else:
        group = Group(name=group_name)
        group.save()
        
    return render(request, 'app/index.html', {'groupname': group_name, 'chats': chats})
