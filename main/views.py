from django.shortcuts import render,redirect

from .models import Article
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import ArticleForm, AuthUserForm, RegisterUserForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.template.loader import render_to_string

class HomeListView(ListView):
    model = Article
    context_object_name = 'list_articles'
    queryset = Article.objects.filter(status=Article.STATUS.PUBLISHED).order_by('-date_pub', 'name')
    paginate_by = 10


class HomeDetailView(DetailView):
    model = Article
    context_object_name = 'get_article'


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)
    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class ArticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Article
    form_class = ArticleForm
    template_name = 'main/article_edit.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись успешно создана'
    def get_context_data(self,**kwargs):
        kwargs['list_articles'] = Article.objects.filter(author=self.request.user).order_by('-id')
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    login_url = reverse_lazy('login_page')
    model = Article
    form_class = ArticleForm
    template_name = 'main/article_edit.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись успешно обновлена'
    def get_context_data(self,**kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class ArticleDeleteView(LoginRequiredMixin, CustomSuccessMessageMixin, DeleteView):
    login_url = reverse_lazy('login_page')
    model = Article
    template_name = 'main/article_edit.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись успешно удалена'
    def post(self, request):
        messages.success(self.request, self.success_msg)
        return super().post(request)
    def delete(self, request):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class ArticleTogglePublic(LoginRequiredMixin, UpdateView):
    # Опубликовать статью / снять
    login_url = reverse_lazy('login_page')
    success_url = reverse_lazy('edit_page')
    model = Article
    def get(self, request, *args, **kwargs):
        user = request.user
        id = kwargs['pk']
        status = bool(kwargs['st'])
        if status:
            Article.objects.filter(id=id,author=user,status=Article.STATUS.DRAFT).update(status=Article.STATUS.PUBLISHED, date_pub=timezone.now())
        else:
            Article.objects.filter(id=id,author=user,status=Article.STATUS.PUBLISHED).update(status=Article.STATUS.DRAFT)
        if request.is_ajax():
            return HttpResponse(render_to_string('main/tags/td_status.html', {'article':self.get_object()}))
        return HttpResponseRedirect(self.success_url)


class ArticleActionView(LoginRequiredMixin, View):
    # Обработка действий
    login_url = reverse_lazy('login_page')
    success_url = reverse_lazy('edit_page')
    def post(self, request):
        action = request.POST.get('action')
        items = request.POST.getlist('_selected_action')
        user = request.user
        row = 0
        if action == 'publish':
            row = Article.objects.filter(id__in=items,author=user,status=Article.STATUS.DRAFT).update(status=Article.STATUS.PUBLISHED, date_pub=timezone.now())
            if row == 1:
                success_msg = "1 запись была опубликована"
            else:
                success_msg = f"{row} записей были опубликованы"
        if action == 'unpublish':
            row = Article.objects.filter(id__in=items, author=user, status=Article.STATUS.PUBLISHED).update(status=Article.STATUS.DRAFT)
            if row == 1:
                success_msg = "1 запись была снята с публикации"
            else:
                success_msg = f"{row} записей были сняты с публикации"
        if action == 'delete':
            row = Article.objects.filter(id__in=items, author=user).delete()[0]
            if row == 1:
                success_msg = "1 запись была удалена"
            else:
                success_msg = f"{row} записей были удалены"
        if row > 0:
            messages.success(self.request, success_msg)
        return HttpResponseRedirect(self.success_url)


class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('edit_page')
    def get_success_url(self):
        return self.success_url


class RegisterUserView(CustomSuccessMessageMixin, CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Пользователь успешно создан'
    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        aut_user = authenticate(username=username,password=password)
        login(self.request, aut_user)
        return form_valid


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('edit_page')