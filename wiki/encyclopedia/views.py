from django.shortcuts import render
from markdown2 import Markdown 
from django import forms

markdowner = Markdown()
class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        context = {
            'page': page_converted,
            'title': title,
             }
        return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found.", "form":Search()})

def search(request):
    search_term =request.GET.get("q","")
    entries = util.list_entries()
    list_wiki = []
    
    for wiki_entry in entries:
        if search_term.lower() in wiki_entry.lower():
            list_wiki.append(wiki_entry)

    context = {
        'search_term': search_term,
        'result': list_wiki
    }
    

    return render(request, "encyclopedia/search.html", context)

def create(request):

    context = {
        "create": False
    }

    if request.method == "POST":
        Title = request.POST.get("Title","")
        Content = request.POST.get("Content","")

        if Title not in util.list_entries():
            context = {
                "Title": Title,
                "Content": Content,
                "create": True,
            }
            util.save_entry(Title, Content)
            return render(request, "encyclopedia/create.html", context)
        else:
            context = {
                "message": "Error: You are trying to create a Wiki entry which already exists.",
            }
            return render(request, "encyclopedia/error.html", context)
    else:
        return render(request, "encyclopedia/create.html", context)


def edit(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        context = {
            'Title': title,
            'Content': page,
            'create': False,
             }
        return render(request, "encyclopedia/create.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "The requested page was not found.", "form":Search()})



    # entries = util.list_entries()
    # if title in entries:
    #     page = util.get_entry(title)
    #     page_converted = markdowner.convert(page)
    #     context = {
    #         'Content': page_converted,
    #         'Title': title,
    #          }
    #     return render(request, "encyclopedia/create.html", context)
    # else:
    #     return render(request, "encyclopedia/error.html", {"message": "The requested page was not found.", "form":Search()})

        