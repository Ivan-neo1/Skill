from django.urls import path
from .views import ProductsList, ArticleCreate, ArticleEdit, NewsDelete

urlpatterns = [

    path('', ProductsList.as_view(), name='article_list'),

    path('create/', ArticleCreate.as_view(), name='create_article'),

    path('<int:pk>/edit/', ArticleEdit.as_view(), name='update_article'),

    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),

]


