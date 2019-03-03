from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import URLForm
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import re


def visible(element):
    # type: (PageElement) -> bool
    """
    Function returns True if element is the part of visible content of the page, False otherwise.
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_url(request):
    """
    View dedicated to get the URL from user.
    """
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            request.session['url'] = form.cleaned_data['url']
            return HttpResponseRedirect(reverse('statistics:statistic'))
    else:
        form = URLForm()
    error = request.session.get('error', False)
    url = request.session.get('url', "")
    if error:
        del request.session['error'], request.session['url']
    return render(request, 'statistics/url.html', {'form': form, 'url': url,'error': error})


def show_statistic(request):
    """
    View dedicated to show statistics for given URL.
    """
    url = request.session.get('url')
    if not url:
        return HttpResponseRedirect(reverse('statistics:url'))
    try:
        page = requests.get(url)
    except requests.ConnectionError:
        request.session['error'] = True
        request.session['url'] = url
        return HttpResponseRedirect(reverse('statistics:url'))
    soup = BeautifulSoup(page.content, 'html.parser')
    meta = soup.find(attrs={"name": re.compile("keywords", re.I)})
    keywords = meta['content'].split(",") if meta else ""
    results = []
    if keywords:
        keywords = (keyword.strip() for keyword in keywords if keyword.strip())
        all_texts = soup.findAll(text=True)
        visible_texts = filter(visible, all_texts)
        text = " ".join(t for t in visible_texts if not t.isspace())
        results = ((keyword, len(re.findall(r"\b" + keyword + r"\b", text))) for keyword in keywords)
    return render(request, 'statistics/statistic.html', {'url': url, 'results': results})
