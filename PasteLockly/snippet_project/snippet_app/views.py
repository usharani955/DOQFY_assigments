from django.shortcuts import render, redirect, get_object_or_404
from .models import Snippet
from .forms import SnippetForm
from django.http import HttpResponse

def create_snippet(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            secret_key = form.cleaned_data['secret_key']
            if secret_key:
                snippet.set_secret_key(secret_key)
                snippet.encrypt_content(secret_key)
            snippet.save()
            return render(request, 'snippet_app/snippet_created.html', {'snippet': snippet})
    else:
        form = SnippetForm()
    return render(request, 'snippet_app/create_snippet.html', {'form': form})

def view_snippet(request, snippet_id):
    snippet = get_object_or_404(Snippet, id=snippet_id)
    if snippet.encrypted:
        if request.method == 'POST':
            secret_key = request.POST.get('secret_key')
            if hashlib.sha256(secret_key.encode()).hexdigest() == snippet.secret_key_hash:
                try:
                    content = snippet.decrypt_content(secret_key)
                    return render(request, 'snippet_app/view_snippet.html', {'content': content})
                except Exception as e:
                    return HttpResponse("Invalid key or decryption error.")
            else:
                return HttpResponse("Invalid key.")
        return render(request, 'snippet_app/enter_key.html')
    return render(request, 'snippet_app/view_snippet.html', {'content': snippet.content})
