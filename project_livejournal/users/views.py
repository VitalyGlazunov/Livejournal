from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from journal.models import Article, Like
from .forms import ProfileImageForm, UserRegisterForm, UserUpdateForm
from .models import Profile


class RegisterView(FormView):
    template_name = 'users/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        messages.success(self.request, f'Пользователь {username} был успешно создан!')
        return super().form_valid(form)


class ProfileSettingsView(LoginRequiredMixin, View):
    template_name = 'users/profile_settings.html'

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


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = Profile.objects.get_or_create(user=user)[0]
        context['user'] = user
        context['profile'] = profile
        article_count = Article.objects.filter(author=user).count()
        context['article_count'] = article_count
        total_likes = Like.objects.filter(article__author=user, like=True, article__publication=True).count()
        context['total_likes'] = total_likes
        return context

