from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostDelete, PostCreate, PostUpdate

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
]
