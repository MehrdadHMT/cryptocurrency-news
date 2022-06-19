from django.urls import path, re_path

from .views import CcNewsListView, CcNewsDetailView, RefreshCrawlerView


urlpatterns = [
	re_path(r'^list/(?P<cat>\w+|)(/|)$', CcNewsListView.as_view(), name='api_ccnews'),
	path('get/<int:pk>/', CcNewsDetailView.as_view(), name='api_ccnews_detail'),
	path('refresh-crawler/', RefreshCrawlerView.as_view(), name='api_refresh_crawler'),
]
