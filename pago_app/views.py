from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
def paymentIndex(request):
    return render(request, 'payment.html')

def paymentSucces(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        return redirect('/inicio/success')
