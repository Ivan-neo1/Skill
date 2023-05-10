from django.urls import path
# Импортируем созданные нами представления
from .views import ProductsList, News_id, PostCreate, NewsEdit, NewsDelete,\
   upgrade_me,  CategoriesView, CategoryDetail, subscribe_to_category

urlpatterns = [
   path('', ProductsList.as_view()),

   path('<int:pk>', News_id.as_view(), name='post_detail'),

   path('create/', PostCreate.as_view(), name='news_create'),

   path('<int:pk>/edit/', NewsEdit.as_view(), name='update_news'),

   path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),

#В случае если при на странице создания поста нажали кнопку "Хочу стать автором"
   path('create/upgrade/', upgrade_me, name='upgrade'),

   path("categories/", CategoriesView.as_view()),
   path("categories/<int:pk>", CategoryDetail.as_view()),
   path("categories/<int:pk>/subscribe", subscribe_to_category),

]


