from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Article, Comment
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
)


# @api_view(["GET", "POST"])
# def article_list(request):
#     if request.method == "GET":
#         articles = Article.objects.all()
#         serializer = ArticleSerializer(articles, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = ArticleSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # data = request.data
#         # title = data.get("title")
#         # content = data.get("content")
#         # article = Article.objects.create(title=title, content=content)
#         # return Response({})


# @api_view(["GET", "PUT", "DELETE"])
# def article_detail(request, pk):
#     if request.method == "GET":
#         article = get_object_or_404(Article, id=pk)
#         serializer = ArticleSerializer(article)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         article = get_object_or_404(Article, id=pk)
#         serializer = ArticleSerializer(article, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

#     elif request.method == "DELETE":
#         article = get_object_or_404(Article, id=pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
    tags=["Articles"],
        description="Article 목록 조회를 위한 API",
    )

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    @extend_schema(
    tags=["Articles"],
        description="Article 생성을 위한 API",
        request=ArticleSerializer,

    )

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(
            article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)  # 바인딩
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, id=comment_pk)

    def put(self, request, comment_pk):
        comment = self.get_object(id=comment_pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = self.get_object(id=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(["GET"])
def check_sql(request):
    from django.db import connection

    articles = Article.objects.all()
    for article in articles:
        comments = article.comments.all().prefedch_related("aritcle")
        for comment in comments:
            print(comment.content)

    print("-" * 30)
    print(connection.queries)

    return Response()