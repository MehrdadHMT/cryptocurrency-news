from django.contrib import admin

from .models import CryptocurrencyNews


class CcNewsAdmin(admin.ModelAdmin):
	list_display = ('title', 'publish_date', 'category')


admin.site.register(CryptocurrencyNews, CcNewsAdmin)
