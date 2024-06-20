from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, ProfileImageForm, UserUpdateForm


class RegisterView(FormView):
    template_name = 'users/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Пользователь {username} был успешно создан!')
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        profile_form = ProfileImageForm(instance=request.user.profile)
        update_user_form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {
            'profileForm': profile_form,
            'updateUserForm': update_user_form
        })

    def post(self, request, *args, **kwargs):
        profile_form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        update_user_form = UserUpdateForm(request.POST, instance=request.user)
        if profile_form.is_valid() and update_user_form.is_valid():
            update_user_form.save()
            profile_form.save()
            messages.success(request, f'Ваш аккаунт был успешно обновлен!')
            return redirect('profile')
        return render(request, self.template_name, {
            'profileForm': profile_form,
            'updateUserForm': update_user_form
        })
