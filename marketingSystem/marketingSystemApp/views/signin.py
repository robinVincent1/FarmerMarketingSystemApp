from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  # Rename the function to avoid conflicts
from .form import UserLoginForm

def login(request):
    """
    View to handle user login.
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)  # Log in the user
                return redirect('home')
            else:
                # Pass the error message directly to the template context
                return render(request, 'signin.html', {
                    'form': form,
                    'error_message': 'Invalid credentials. Please try again.'
                })
    else:
        form = UserLoginForm()  # Create an empty form instance
    return render(request, 'signin.html', {'form': form})
