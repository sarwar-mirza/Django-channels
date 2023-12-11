from django.shortcuts import render
from .models import Chat, Group

# Create your views here.
def index(request, group_name):
    print('Group Name :', group_name)     # check Debuging
    
    # Save your group activities to the database
    name_group = Group.objects.filter(name=group_name).first()     #filter group name
    
    chats = []      # list
    if name_group:
        chats = Chat.objects.filter(group= name_group)         # check models group = 
    else:
        group = Group(name=group_name)
        group.save()
    
    return render(request, 'app/index.html', {'groupname': group_name, 'chats': chats})
