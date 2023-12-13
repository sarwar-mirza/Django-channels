from django.shortcuts import render

# Ex-02(real time)
def index(request):
    return render(request, 'app/realtime.html')
