from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method != 'POST':
        from_ = UserCreationForm()

    else:
        from_ = UserCreationForm(data=request.POST)

        if from_.is_valid():
            new_user = from_.save()
            login(request, new_user)
            return redirect('learning_log:index')

    context = {'from': from_}
    return render(request, 'registration/register.html', context)
