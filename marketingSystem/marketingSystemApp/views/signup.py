from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .form import CustomUserCreationForm  # Ensure the file name is correct

def register(request):
    """
    View to handle user registration.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log in the new user
            return redirect('home')
        else:
            # Handle form errors
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()  # Create an empty form instance
        return render(request, 'signup.html', {'form': form})
