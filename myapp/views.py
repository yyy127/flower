from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # return render(request, 'myapp/home.html')
    result = subprocess.run(['python', 'myapp/receipt.py'], capture_output=True, text=True)
    return HttpResponse(result.stdout)