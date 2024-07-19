from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortURL
from .forms import URLForm

def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            short_url = form.save()
            return render(request, 'urlshortener_app/url_created.html', {'short_url': short_url})
    else:
        form = URLForm()
    return render(request, 'urlshortener_app/home.html', {'form': form})

def redirect_url(request, short_url):
    short_url_obj = get_object_or_404(ShortURL, short_url=short_url)
    return redirect(short_url_obj.original_url)
