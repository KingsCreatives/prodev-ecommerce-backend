from django.shortcuts import render

def index(request):
    """
    Renders the API landing page.
    """
    return render(request, 'index.html')