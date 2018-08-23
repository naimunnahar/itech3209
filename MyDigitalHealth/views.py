from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import RegistrationForm, CreateCardPackage, CreateCardGroup, CreateCards, CreateComments
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import Package, Category, Card, Comment
from django.template.response import TemplateResponse
from django.contrib import messages 


def index(request):
    """
    View function for home page of site.
    View function for home page of site.
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_visits': num_visits},  # num_visits appended
    )


def create(request):
    return render(
        request,
        'project.html',
    )


def cards(request):
    if request.method == 'POST':
        form = CreateCardPackage(request.POST, instance=Package())
        if form.is_valid():
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            groups = request.POST.getlist('group')
            names = request.POST.getlist('name')
            user = request.user
            for name in names:
                cardPackage = Package(name=name, user=user)
                cardPackage.save()
            for title in titles:
                group = Category(card_package=cardPackage, title=title)
                group.save()
            for text in texts:
                card = Card(card_package=cardPackage, card_group=group, text=text)
                card.save()
            return render(
                request,
                'index.html',
            )
        else:
            form = CreateCardPackage(instance=Package())
            args = {'form': form}
            return render(
                request,
                'project.html',
                {'form': form}
            )
    else:
        form = CreateCardPackage(instance=Package())
        args = {'form': form}
        return render(
            request,
            'project.html',
            {'form': form}
        )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(
                request,
                'index.html',
            )
        else:
            form = RegistrationForm()
            args = {'form': form}
            return render(
                request,
                'register.html',
                {'form': form}
            )
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(
            request,
            'register.html',
            {'form': form}
        )


def view(request):
    cardPackages = Package.objects.all()
    return render(
        request,
        'view.html',
    )


def package(request):
    cardPackages = Package.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'package.html',
        context
    )


def packageList(request, package):
    package = Package.objects.get(id__exact=package)
    context = {'package': package}
    return render(
        request,
        'packageList.html',
        context
    )


def admin(request):
    cardPackages = Package.objects.all()
    context = {'cardPackages': cardPackages}
    return render(
        request,
        'admin.html',
        context
    )


def edit(request, package):
    package = Package.objects.get(id__exact=package)
    context = {'package': package}
    return render(
        request,
        'edit.html',
        context
    )


def comments(request):
    if request.method =='POST':
        form = CreateComments(request.POST, instance=Comment())
        name = request.POST.get('name')
        cardPackage = Package.objects.get(name = name)
        user = request.user
        comment = request.POST.get('comment')
        comments = Comment(card_package = cardPackage, user = user, comment = comment)
        comments.save()
        return render(
            request,
            'index.html',
        )
    else:
        form = CreateCardPackage(instance=Comment())
        args = {'form': form}
        return render(
            request,
            'packageList.html',
            {'form': form}
        )


def editPackage(request, package):
    if request.method == 'POST':
        form = CreateCardPackage(request.POST, instance=Package())
        if form.is_valid():
            cardPackage = Package.objects.get(id__exact=package)
            titles = request.POST.getlist('title')
            texts = request.POST.getlist('text')
            cardGroupIDs = request.POST.getlist('cardGroupID')
            cardListIDs = request.POST.getlist('cardListID')
            name = request.POST.get('name')
            user = request.user
            cardPackage.name = name
            cardPackage.save()
            group = Category()
            card = Card()
            for cardGroupID, title in zip(cardGroupIDs, titles):
                group.id = cardGroupID
                group.card_package = cardPackage
                group.title = title
                group.save()
            for cardListID, text in zip(cardListIDs, texts):
                card.id = cardListID
                card.card_package = cardPackage
                card.card_group = group
                card.text = text
                card.save()
            return render(
                request,
                'admin.html',
            )
        else:
            form = CreateCardPackage(instance=Package())
            args = {'form': form}
            return render(
                request,
                'admin.html',
                {'form': form}
            )
    else:
        form = CreateCardPackage(instance=Package())
        args = {'form': form}
        return render(
            request,
            'admin.html',
            {'form': form}
        )


def cardPackages(request):
    cardPackages = Package.objects.all()
    return TemplateResponse(request, views.index, {'cardPackages': cardPackages})


def cardGroups(request):
    cardGroups = Category.objects.all()
    return TemplateResponse(request, views.index, {'cardGroups': cardGroups})


def cardList(request):
    cardList = Card.objects.all()
    return TemplateResponse(request, views.index, {'cardList': cardList})
