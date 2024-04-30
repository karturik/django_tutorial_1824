from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm
from .forms import UserEditForm, ProfileEditForm
from .models import Profile


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("books")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "registration.html", context={"register_form": form})


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        return redirect("profile_page", request.user.profile.pk)

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'edit.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


class ProfileDetailView(generic.DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile_page.html'

