from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealer_reviews_from_cf, post_dealer_review
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.user.is_authenticated:
        return redirect('/djangoapp')

    error = None

    if request.method == 'POST':
        try:
            username = request.POST['username'].lower()
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/djangoapp')
            else:
                error = 'INVALID_LOGIN'
        except:
            error = 'LOGIN_FAILED'

    context = { "error": error }
    return render(request, 'djangoapp/login.html', context)    

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('/djangoapp')    

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    error = None

    if request.method == 'POST':
        try:
            username = request.POST['username'].lower()
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            password = request.POST['password']

            try:
                user_exists = User.objects.get(username=username)

                if user_exists:
                    error = 'USERNAME_IN_USE'
                    raise Exception("USERNAME_IN_USE")
            except:
                pass

            user = User.objects.create_user(username, "", password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            if user is not None:
                login(request, user)
                return redirect('/djangoapp')
        except Exception as e:
            print(e)
            if error is None:
                error = 'REGISTER_FAILED'

    context = { "error": error }
    return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}

    url = "https://us-south.functions.appdomain.cloud/api/v1/web/965a5017-3109-4e6f-af1f-3388fd303def/dealership-package/get-dealership"
    dealerships = get_dealers_from_cf(url)

    context['dealerships'] = dealerships
        
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    
    try:
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/965a5017-3109-4e6f-af1f-3388fd303def/dealership-package/get-dealership"
        dealership = get_dealer_by_id(url, id=dealer_id)
        context['dealership'] = dealership

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/965a5017-3109-4e6f-af1f-3388fd303def/dealership-package/get-reviews"
        reviews = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        context['reviews'] = reviews
    except:
        return redirect('/djangoapp')

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"/djangoapp/dealer/{dealer_id}")
        
        if request.user.is_staff:
            return redirect(f"/djangoapp/dealer/{dealer_id}")

        try:
            url = "https://us-south.functions.appdomain.cloud/api/v1/web/965a5017-3109-4e6f-af1f-3388fd303def/dealership-package/get-dealership"
            dealership = get_dealer_by_id(url, id=dealer_id)
        except:
            return redirect("/djangoapp")

        url = "https://us-south.functions.appdomain.cloud/api/v1/web/965a5017-3109-4e6f-af1f-3388fd303def/dealership-package/get-reviews"
        data = {
            "name": f"{request.user.first_name} {request.user.last_name}",
            "dealership": dealership.id,
            "review": request.POST['review'],
            "purchase": False
        }

        print(data)

        try:
            post_dealer_review(url, data=data)
        except:
            return redirect(f"/djangoapp/dealer/{dealer_id}?error=ADD_REVIEW_ERROR")

    return redirect(f"/djangoapp/dealer/{dealer_id}")

