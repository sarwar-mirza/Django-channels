from django.shortcuts import render

# Create your views here.
def websocketView(request):
    return render(request, 'app/index.html')
