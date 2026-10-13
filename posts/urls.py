from django.urls import path

from posts.views import CategoryPostListView, PostDetailView, PostListView

urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name="category"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
]
