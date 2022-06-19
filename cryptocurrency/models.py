from django.db import models


class CryptocurrencyNews(models.Model):
    BITCOIN = 'btc'
    ALTCOIN = 'atc'
    ETHEREUM = 'eth'
    CRYPTOCURRENCIES = [
        (BITCOIN, 'Bitcoin'),
        (ETHEREUM, 'Ethereum'),
        (ALTCOIN, 'Altcoin'),
    ]

    category = models.CharField(max_length=3, choices=CRYPTOCURRENCIES, default=BITCOIN)
    title = models.CharField(max_length=255)
    description = models.TextField()
    source = models.URLField()
    path = models.CharField(max_length=225, unique=True)
    author = models.CharField(max_length=50)
    publish_date = models.DateTimeField()

    def __str__(self):
        return self.title
