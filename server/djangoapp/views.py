from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Some URL's used in a few functions
get_dealers_url = "https://us-east.functions.appdomain.cloud/api/v1/web/1cfbe9e3-8546-4423-859a-d20b06dd9b6c/dealership-package/get-dealership.json"
get_reviews_url = "https://us-east.functions.appdomain.cloud/api/v1/web/1cfbe9e3-8546-4423-859a-d20b06dd9b6c/dealership-package/get-review.json"
post_review_url = "https://us-east.functions.appdomain.cloud/api/v1/web/1cfbe9e3-8546-4423-859a-d20b06dd9b6c/dealership-package/post-review"


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Check if credentials are valid
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, login user and refresh page
            login(request, user)
            return redirect('/djangoapp/')
        else:
            return redirect('/djangoapp/')
    else:
        return redirect('/djangoapp/')
    # this method needs updating to tell the user that there was an issue with logging in


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('/djangoapp/')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If this is a get request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists.
            User.objects.get(username=username)
            user_exist = True
        except:
            # If user does not exist, then create new user
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect('/djangoapp/')
        else:
            # Should also return an error message saying user already exists
            return render(request, "djangoapp/registration.html", context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    # context = {}
    # if request.method == "GET":
    #    return render(request, 'djangoapp/index.html', context)
    if request.method == "GET":
        dealerships = get_dealers_from_cf(get_dealers_url)
        context = {"dealerships": dealerships}
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer = get_dealer_by_id_from_cf(get_dealers_url, id)
        context["dealer"] = dealer
        reviews = get_dealer_reviews_from_cf(get_reviews_url, id=id)
        print(reviews)
        context["reviews"] = reviews

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, id):
    if request.user.is_authenticated:
        context = {}
        dealer = get_dealer_by_id_from_cf(get_dealers_url, id)
        context["dealer"] = dealer
        if request.method == "GET":
            cars = CarModel.objects.all()
            context["cars"] = cars
            print(context)
            return render(request, 'djangoapp/add_review.html', context)

        if request.method == "POST":
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            form = request.POST
            review["delaership"] = id
            review["review"] = form["content"]
            if form.get("purchasecheck") == "on":
                review["purchase"] = True
            else:
                review["purchase"] = False
            if review["purchase"]:
                review["purchase_date"] = datetime.striptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year
            json_payload = {"review": review}
            post_request(post_review_url, json_payload, id=id)
            return redirect("djangoapp:dealer_details", id=id)
    else:
        return redirect("/djangoapp/login")     # This does not exist yet!!!

