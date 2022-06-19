from rest_framework import serializers

from cryptocurrency.models import CryptocurrencyNews


class CcNewsListSerializer(serializers.ModelSerializer):
	category = serializers.CharField(source='get_category_display')

	class Meta:
		model = CryptocurrencyNews
		fields = ['id', 'category', 'title']
		read_only_fields = ['title', 'category', 'description', 'author', 'publish_date', 'source']


class CcNewsDetailSerializer(CcNewsListSerializer):
	class Meta:
		model = CryptocurrencyNews
		fields = '__all__'
		read_only_fields = ['title', 'category', 'description', 'author', 'publish_date', 'source']
