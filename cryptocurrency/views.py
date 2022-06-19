import os

from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView

from .serializers import CcNewsListSerializer, CcNewsDetailSerializer
from .models import CryptocurrencyNews


class CcNewsListView(generics.ListAPIView):
	serializer_class = CcNewsListSerializer

	def get_queryset(self):
		cat = self.kwargs.get('cat')
		news = CryptocurrencyNews.objects.all()
		if cat:
			return news.filter(category=cat)
		else:
			return news


class CcNewsDetailView(generics.RetrieveAPIView):
	queryset = CryptocurrencyNews.objects.all()
	serializer_class = CcNewsDetailSerializer


class RefreshCrawlerView(APIView):
	def get(self, request):
		os.system("python manage.py crawl >> ./log-files/crawl-command.log 2>&1")
		return Response(status=status.HTTP_200_OK)
