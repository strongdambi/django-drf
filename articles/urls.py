from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    # path("", views.article_list, name="article_list"),
    # path("<int:pk>/", views.article_detail, name="article_detail"),
    
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:article_pk>/comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("comments/<int:comment_pk>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
    path("check-sql/", views.check_sql, name="check_sql"),
]