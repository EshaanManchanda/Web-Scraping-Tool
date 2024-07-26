from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
import pandas as pd
from .forms import ScrapeForm
from .models import ScrapedData, ScrapeHistory
from .scraper import perform_scraping

def index(request):
    form = ScrapeForm()
    return render(request, 'scraper/index.html', {'form': form})

def scrape_data(request):
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        
        if form.is_valid():
            # Perform the scraping operation
            scraped_data = perform_scraping(form.cleaned_data)
            
            # Save the scraping history
            history = ScrapeHistory.objects.create(
                url=form.cleaned_data['url'],
                item_selector=form.cleaned_data['item_selector'],
                title_selector=form.cleaned_data['title_selector'],
                price_selector=form.cleaned_data['price_selector']
            )
            
            # Save each scraped item to the database
            for item in scraped_data:
                ScrapedData.objects.create(
                    url=form.cleaned_data['url'],
                    item_selector=form.cleaned_data['item_selector'],
                    title_selector=form.cleaned_data['title_selector'],
                    price_selector=form.cleaned_data['price_selector'],
                    title=item['title'],
                    price=item['price']
                )
            
            return render(request, 'scraper/results.html', {'data': scraped_data})
        else:
            # Render the form with errors
            return render(request, 'scraper/index.html', {'form': form})
    return HttpResponse("Method not allowed", status=405)

def scrape_history(request):
    history = ScrapeHistory.objects.all().order_by('-scraped_at')
    return render(request, 'scraper/history.html', {'history': history})

def scrape_detail(request, pk):
    history = get_object_or_404(ScrapeHistory, pk=pk)
    data = ScrapedData.objects.filter(url=history.url, item_selector=history.item_selector, title_selector=history.title_selector, price_selector=history.price_selector)
    return render(request, 'scraper/detail.html', {'history': history, 'data': data})

def scrape_delete(request, pk):
    history = get_object_or_404(ScrapeHistory, pk=pk)
    if request.method == 'POST':
        history.delete()
        ScrapedData.objects.filter(url=history.url, item_selector=history.item_selector, title_selector=history.title_selector, price_selector=history.price_selector).delete()
        return redirect('scraper:scrape_history')
    return render(request, 'scraper/confirm_delete.html', {'history': history})

def scrape_update(request, pk):
    history = get_object_or_404(ScrapeHistory, pk=pk)
    if request.method == 'POST':
        form = ScrapeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            item_selector = form.cleaned_data['item_selector']
            title_selector = form.cleaned_data['title_selector']
            price_selector = form.cleaned_data['price_selector']

            # Update history record
            history.url = url
            history.item_selector = item_selector
            history.title_selector = title_selector
            history.price_selector = price_selector
            history.save()

            # Clear existing scraped data
            ScrapedData.objects.filter(url=history.url, item_selector=history.item_selector, title_selector=history.title_selector, price_selector=history.price_selector).delete()

            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                data = []
                for item in soup.select(item_selector):
                    title = item.select_one(title_selector).text.strip()
                    price = item.select_one(price_selector).text.strip()
                    data.append({'Title': title, 'Price': price})
                    # Save each item to the database
                    ScrapedData.objects.create(
                        url=url,
                        item_selector=item_selector,
                        title_selector=title_selector,
                        price_selector=price_selector,
                        title=title,
                        price=price
                    )
                if not data:
                    return render(request, 'scraper/results.html', {'form': form, 'error': 'No data found with the provided selectors.'})

                df = pd.DataFrame(data)
                table_html = df.to_html(index=False)
                return render(request, 'scraper/results.html', {'form': form, 'table': table_html})

            except requests.exceptions.RequestException as e:
                return render(request, 'scraper/results.html', {'form': form, 'error': f"Failed to retrieve the web page: {e}"})
    else:
        form = ScrapeForm(initial={'url': history.url, 'item_selector': history.item_selector, 'title_selector': history.title_selector, 'price_selector': history.price_selector})
    return render(request, 'scraper/update.html', {'form': form, 'history': history})

def export_csv(request):
    if request.method == 'POST':
        data = ScrapedData.objects.all().values()
        df = pd.DataFrame(data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="scraped_data.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response
    return HttpResponse("Invalid request")
