from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    if request.method == 'POST':
        code = request.POST.get('access_code')
        # Basic validation
        if len(code) == 8:  # Example: 8-character code
            return redirect('success')
        return render(request, 'main/index.html', {'error': 'Invalid code format'})
    return render(request, 'main/index.html')

def success(request):
    return render(request, 'main/success.html')