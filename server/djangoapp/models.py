from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=250)
    # logo = models.ImageField()

    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    Sedan = 'Sedan'
    SUV = 'SUV'
    Wagon = 'Wagon'
    Hatch_Back = 'Hatch_Back'
    Convertible = 'Convertible'
    Pickup = 'Pickup'
    Van = 'Van'
    TYPE_CHOICES = [
        (Sedan, 'Sedan'),
        (SUV, 'SUV'),
        (Wagon, 'Wagon'),
        (Hatch_Back, 'Hatch Back'),
        (Pickup, 'Pickup'),
        (Van, 'Van')
    ]
    name = models.CharField(max_length=20)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase    # Should be True or False
        self.review = review
        self.purchase_date = None
        self.car_make = None
        self.car_model = None
        self.car_year = None
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return f"{self.name} left the following {self.sentiment} review: {self.review}"

    def add_car(self, car_make, car_model, car_year, purchase_date):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.purchase_date = purchase_date
