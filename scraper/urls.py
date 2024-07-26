from django.urls import path
from . import views

app_name = 'scraper'

urlpatterns = [
    path('', views.index, name='index'),  # URL for the form page
    path('scrape/', views.scrape_data, name='scrape_data'),  # URL for scraping data
    path('export_csv/', views.export_csv, name='export_csv'),
    path('history/', views.scrape_history, name='scrape_history'),
    path('history/<int:pk>/', views.scrape_detail, name='scrape_detail'),
    path('history/<int:pk>/delete/', views.scrape_delete, name='scrape_delete'),
    path('history/<int:pk>/update/', views.scrape_update, name='scrape_update'),
]
