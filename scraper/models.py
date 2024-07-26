from django.db import models

class ScrapedData(models.Model):
    url = models.URLField()
    item_selector = models.CharField(max_length=200)
    title_selector = models.CharField(max_length=200)
    price_selector = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    price = models.CharField(max_length=200)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ScrapeHistory(models.Model):
    url = models.URLField()
    item_selector = models.CharField(max_length=200)
    title_selector = models.CharField(max_length=200)
    price_selector = models.CharField(max_length=200)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
