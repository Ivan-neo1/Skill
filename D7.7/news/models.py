
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0)

    def update_rating(self):
        post_r = Post.objects.filter(author_id=self.id)
        comment_r = Comment.objects.filter(user_id=self.user.id)
        w = 0
        for i in comment_r:
            w += i.rating_comment
        x = 0
        for post in post_r:
            x += post.rating_art_nws

        self.rating_user = x * 3 + self.rating_user + w
        self.save()



class Category(models.Model):
    cat = models.CharField(max_length=64, default="Default value", unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author,
                               related_name='posts',
                               related_query_name='post',
                               on_delete=models.CASCADE)
    article = 'ART'
    news = 'NWS'
    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    article_or_news = models.CharField(max_length=3, choices=POSITIONS, default=None)
    time_in = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=200, default='Заголовок отсутствует')
    text = models.TextField(default='Текст отсутствует')
    rating_art_nws = models.IntegerField(default=0)

    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating_art_nws = self.rating_art_nws + 1
        self.save()

    def dislike(self):
        self.rating_art_nws = self.rating_art_nws - 1
        self.save()

    def preview(self):
        return self.text[0: 124] + "…"

    def __str__(self):
        return f'{self.author}, {self.header}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])



class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField(default="Комментарий отсутствует")
    time_in = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment = self.rating_comment + 1
        self.save()

    def dislike(self):
        self.rating_comment = self.rating_comment - 1
        self.save()
