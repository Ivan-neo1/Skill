from django.urls import path
# Импортируем созданные нами представления
from .views import ProductsList, News_id, PostCreate, NewsEdit, NewsDelete

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', ProductsList.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', News_id.as_view(), name='post_detail'),

   path('create/', PostCreate.as_view(), name='news_create'),

   path('<int:pk>/edit/', NewsEdit.as_view(), name='update_news'),

   path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),


]


