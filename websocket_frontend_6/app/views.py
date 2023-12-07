from django.shortcuts import render

# Create your views here.
def websocketview(request):
    return render(request, 'app/index.html')
