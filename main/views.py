# main/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserSubmission

VALID_CASE_IDS = {
    'APL-2024-1234',
    'APL-2024-5678',
    'APL-2024-9123'
}

def index(request):
    error = None
    if request.method == 'POST':
        # Get case ID from POST data
        case_id = request.POST.get('case_id', '').strip()
        
        if case_id in VALID_CASE_IDS:
            # Store verification in session
            request.session['verified_case'] = case_id
            request.session.modified = True  # Force session save
            return redirect('terms_of_use')
        else:
            error = "Invalid Case ID. Please check your entry."
    
    return render(request, 'main/index.html', {'error': error})

def terms_of_use(request):
    # Check session verification
    if not request.session.get('verified_case'):
        return redirect('index')
    return render(request, 'main/terms_of_use.html')


def Idusername(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        
        # Create new submission
        UserSubmission.objects.create(name=full_name)
        
        messages.success(request, f"Name '{full_name}' successfully recorded!")
        return redirect('idpassword')  # Will implement number collection next
        
    return render(request, 'main/idpassword.html')

def collect_number(request):
    # Will implement number collection next
    return render(request, 'main/number_collection.html')
