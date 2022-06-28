from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostDelete, PostCreate, PostUpdate, make_author, ProfileUpdate, Subscribe

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view()),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('upgrade/', make_author, name='upgrade'),
    path('profile/', ProfileUpdate.as_view(), name='profile_update'),
    path('subscribe/', Subscribe.as_view(), name='subscribe'),
]
