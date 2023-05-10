from django.core.mail import send_mail
from .models import Category, CategorySubscribe, Post
from datetime import datetime
from .models import User
from django.template.loader import render_to_string
from django.core.mail import send_mail
from celery import shared_task
import time
from celery import shared_task
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed



def send_weekly(instance, action,):

    week_number_last = datetime.now().isocalendar()[1]
    week_posts = Post.objects.filter(created_at__week=str(week_number_last))
    categories1 = Category.objects.all()

    categories_str = []
    for category in categories1:
        categories_str.append(category.cat)

    print(categories_str)

    subscribed_users = []
    for category_subscribe in CategorySubscribe.objects.filter(category__in=instance.categories.all()):
        subscribed_users.append(category_subscribe.subscriber.email)
        posts_of_category = week_posts.filter(post_category_id=category.id)


        for user in subscribed_users:

            print(user)

            message = ''
            for post in posts_of_category:
                message += post.post_text + f'http://127.0.0.1:8000/{post.id}' + '\n'

            send_mail(
                subject=f'Посты за неделю в категории {Category.objects.get(id=category.id)}',
                html_message=render_to_string('weekly_posts.html', context={'link': f'http://127.0.0.1:8000/news/',
                                                                            'user': User.objects.get(
                                                                                id=user.subscriber_id),
                                                                            'category': Category.objects.get(
                                                                                id=category.id),
                                                                            'posts': posts_of_category}),
                message='',
                from_email='dagson00066@yandex.ru',
                recipient_list=subscribed_users,
            )


@shared_task
def send_fresh_news_list_to_subs():
    categories = Category.objects.all()
    week_ago = timezone.now() - timedelta(days=7)
    fresh_news = Post.objects.filter(creation_time__gt=week_ago)

    for category in categories:
        fresh_news_in_category = fresh_news.filter(categories=category)
        recipients = []
        for subscriber in category.subscribers.all():
            recipients.append(subscriber.email)
        html_content = render_to_string('mail_news_list.html', {'news': fresh_news_in_category})
        msg = EmailMultiAlternatives(
            subject="Свежие новости за неделю",
            from_email='dagson00066@yandex.ru',
            to=recipients,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()












