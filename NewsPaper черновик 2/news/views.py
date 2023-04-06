from django.views.generic import ListView, DetailView, CreateView,\
    UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .filters import PostFilter
from .models import Post, Category, CategorySubscribe, User
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import send_mail
from django.db.models.signals import post_save

class ProductsList(ListView):
    model = Post
    ordering = 'author'
    template_name = 'news.html'
    context_object_name = 'post'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class News_id(DetailView):
    model = Post
    ordering = '-creation_time'
    template_name = 'news_id.html'
    context_object_name = 'post_id'

class PostCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        news = form.save(commit=False)
        news.article_or_news = 'NWS'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

class ArticleCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'
    permission_required = ('article.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

    def form_valid(self, form):
        article = form.save(commit=False)
        article.article_or_news = 'ART'
        return super().form_valid(form)
#При создании поста после авторизации будет появляться кнопка "Хочу стать автором"
@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news/')

class NewsEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.change_post',)

class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')

class ArticleEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'
    permission_required = ('article.change_post',)




class CategoriesView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'categories.html', {'categories': Category.objects.all()})

class CategoryDetail(LoginRequiredMixin, DetailView):

    model = Category
    template_name = 'category.html'
    context_object_name = 'category'


def subscribe_to_category(request, pk):

    current_user = request.user
    CategorySubscribe.objects.create(category=Category.objects.get(pk=pk), subscriber=User.objects.get(pk=current_user.id))

    return render(request, 'subscribed.html')


def notify_new_post_in_category(instance, **kwargs):

    category_id = instance.categories.id

    subscribed_users = []
    subscribed_users_1 = CategorySubscribe.objects.filter(category_id=int(category_id))

    for user in subscribed_users_1:
        subscribed_users.append(User.objects.get(id=user.subscriber_id).email)

    print(subscribed_users)

    send_mail(
        subject=f'Здравствуй. Новая статья в твоём любимом разделе! {Category.objects.get(id=category_id)}',
        message="Hello",
        from_email='dagson00066@yandex.ru',
        recipient_list=subscribed_users
    )

post_save.connect(notify_new_post_in_category, sender=Post)

#send_mail(
#    subject=f'Здравствуй. Новая статья в твоём любимом разделе! {Category.objects.get(id=category_id)}',
#    html_message=render_to_string('new_post.html',
#                                  context={'post': instance, 'category': Category.objects.get(id=category_id).cat,
#                                           'link': f'http://127.0.0.1:8000/{instance.id}'}),
#    message='',
#    from_email='dagson00066@yandex.ru',
#    recipient_list=subscribed_users
#)